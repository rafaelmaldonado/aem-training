#!/usr/bin/env python3
"""Build and install the local-only workflow package into the SDK Author."""

import base64
import json
import os
import subprocess
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "http://localhost:4502"
PACKAGE = ROOT / "local-tools/workflow/package/target/assets.local.workflow.package-1.0.0-SNAPSHOT.zip"
MODEL = "/conf/global/settings/workflow/models/assets-local-jpeg-800/jcr:content"


def request(path, password, data=None, content_type=None, token=None):
    headers = {
        "Authorization": "Basic " + base64.b64encode(("admin:" + password).encode()).decode()
    }
    if content_type:
        headers["Content-Type"] = content_type
    if token:
        headers["CSRF-Token"] = token
    with urllib.request.urlopen(urllib.request.Request(BASE + path, data=data, headers=headers), timeout=120) as response:
        return response.read()


def multipart(fields, filename, contents):
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="package"; '
                  f'filename="{filename}"\r\nContent-Type: application/zip\r\n\r\n').encode())
    parts.extend((contents, f'\r\n--{boundary}--\r\n'.encode()))
    return b"".join(parts), "multipart/form-data; boundary=" + boundary


def main():
    password = os.environ.get("AEM_ADMIN_PASSWORD") or (ROOT.parent / "author/.admin-password").read_text().strip()
    subprocess.run([str(ROOT / "mvnw"), "-f", str(ROOT / "local-tools/workflow/pom.xml"),
                    "clean", "package", "-q"], cwd=ROOT, check=True)
    token = json.loads(request("/libs/granite/csrf/token.json", password))["token"]
    body, content_type = multipart({"cmd": "upload", "force": "true"}, PACKAGE.name, PACKAGE.read_bytes())
    uploaded = json.loads(request("/crx/packmgr/service/.json", password, body, content_type, token))
    if not uploaded.get("success") or not uploaded.get("path"):
        raise RuntimeError(f"No se pudo subir el paquete: {uploaded}")
    path = urllib.parse.quote(uploaded["path"], safe="/")
    installed = json.loads(request("/crx/packmgr/service/.json" + path, password,
                                   b"cmd=install", "application/x-www-form-urlencoded", token))
    if not installed.get("success"):
        raise RuntimeError(f"No se pudo instalar el paquete: {installed}")
    request(MODEL + ".generate.json", password, b"", "application/x-www-form-urlencoded", token)
    print("Workflow local instalado y sincronizado en el Author: " + MODEL)


if __name__ == "__main__":
    main()
