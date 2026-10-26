#!/usr/bin/env python3
"""Generate the configured DAM rendition in the local AEM SDK (macOS only)."""

import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree


FOLDER = "/content/dam/assets"
PROFILE_PATH = "/conf/global/settings/dam/processing/assets-jpeg-800"
AUTHOR = "http://localhost:4502"
PROFILE = Path(__file__).resolve().parents[1] / "ui.content/src/main/content/jcr_root/conf/global/settings/dam/processing/assets-jpeg-800/jpeg-800/.content.xml"
PASSWORD_FILE = Path(__file__).resolve().parents[2] / "author/.admin-password"


def main():
    if len(sys.argv) != 2:
        raise ValueError("Uso: python3 local-tools/generate-rendition.py /content/dam/assets/imagen.jpg")
    asset = sys.argv[1]
    if not asset.startswith(FOLDER + "/") or any(part in ("", ".", "..") for part in asset.split("/")[1:]):
        raise ValueError("El asset debe estar dentro de /content/dam/assets")
    if sys.platform != "darwin":
        raise RuntimeError("Este workaround local usa sips de macOS")

    config = ElementTree.parse(PROFILE).getroot()[0].attrib
    name = config["name"]
    max_width, max_height = int(config["wid"]), int(config["hei"])
    password = os.environ.get("AEM_ADMIN_PASSWORD") or PASSWORD_FILE.read_text().strip()
    auth = "Basic " + base64.b64encode(("admin:" + password).encode()).decode()

    def send(path, method="GET", data=None, content_type=None):
        headers = {"Authorization": auth}
        if content_type:
            headers["Content-Type"] = content_type
        request = Request(AUTHOR + quote(path, safe="/"), data=data, headers=headers, method=method)
        return urlopen(request, timeout=30)

    with send(FOLDER + "/jcr:content.json") as response:
        if json.load(response).get("processingProfile") != PROFILE_PATH:
            raise RuntimeError("La carpeta local no tiene asignado Assets JPEG 800")

    with TemporaryDirectory() as directory:
        original = Path(directory) / ("original" + Path(asset).suffix)
        rendition = Path(directory) / name
        with send(asset + "/jcr:content/renditions/original") as response:
            if not re.fullmatch(config["includeMimeTypes"], response.headers.get_content_type()):
                raise ValueError("El asset no es una imagen")
            original.write_bytes(response.read())

        dimensions = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(original)],
            check=True, capture_output=True, text=True,
        ).stdout
        size = re.findall(r"pixel(?:Width|Height): (\d+)", dimensions)
        if len(size) != 2:
            raise ValueError("sips no pudo leer las dimensiones de la imagen")
        width, height = map(int, size)
        command = ["sips", "-s", "format", config["fmt"], "-s", "formatOptions", config["qlt"]]
        scale = min(1, max_width / width, max_height / height)
        if scale < 1:
            command += ["-z", str(max(1, round(height * scale))), str(max(1, round(width * scale)))]
        subprocess.run(command + [str(original), "--out", str(rendition)], check=True, capture_output=True)

        endpoint = "/api/assets" + asset.removeprefix("/content/dam") + "/renditions/" + name
        payload = rendition.read_bytes()
        try:
            with send(endpoint, method="PUT", data=payload, content_type="image/jpeg") as response:
                status = response.status
        except HTTPError as error:
            if error.code != 404:
                raise
            with send(endpoint, method="POST", data=payload, content_type="image/jpeg") as response:
                status = response.status
        print(f"HTTP {status}: {asset}/jcr:content/renditions/{name}")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"Error: {error}")
