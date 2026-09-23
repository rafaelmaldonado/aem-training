#!/usr/bin/env python3
"""Generate the missing Session 29 slides through the OpenAI Images API."""

from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "slides/lesson-29"
SKILL_ROOT = Path.home() / ".codex/skills/codex-ppt"
RUNTIME_PYTHON = Path.home() / ".codex-ppt-skill/.venv/bin/python"
IMAGEGEN = SKILL_ROOT / "scripts/image_gen.py"
RECORD_DISPATCH = SKILL_ROOT / "scripts/record_slide_dispatch.py"
RECORD_RESULT = SKILL_ROOT / "scripts/record_slide_result.py"
RECORD_BLOCKER = SKILL_ROOT / "scripts/record_slide_blocker.py"
RUNTIME_ENV = Path.home() / ".codex-ppt-skill/.env"


def parse_slides(value: str) -> list[int]:
    numbers: set[int] = set()
    for part in value.split(","):
        bounds = part.strip().split("-", 1)
        start = int(bounds[0])
        end = int(bounds[-1])
        numbers.update(range(start, end + 1))
    if not numbers or min(numbers) < 4 or max(numbers) > 12:
        raise argparse.ArgumentTypeError("slides must be between 4 and 12")
    return sorted(numbers)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(value)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def run(command: list[str]) -> None:
    process = subprocess.Popen(
        command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output = []
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
        output.append(line)
    if process.wait():
        detail = "".join(output).strip()
        raise RuntimeError(detail or "Command failed")


def prepare_api_state(slide: int, model: str, size: str, quality: str) -> None:
    jobs_path = DECK / "slide_jobs.json"
    jobs = read_json(jobs_path)
    jobs["selected_backend"] = "scripts/image_gen.py (OpenAI API)"
    jobs["sample_generation_method"] = {
        "backend_used": "scripts/image_gen.py (OpenAI API)",
        "tool_name": "scripts/image_gen.py",
        "mode": "edit",
        "model": model,
        "size": size,
        "quality": quality,
        "approved_sample_path": str(ROOT / "slides/lesson-28/origin_image/slide_04.png"),
        "prompt_source": "slides/lesson-29/prompts/slide_XX.json",
        "input_context_preparation": "Lesson 28 slide 04 supplied as a style-only image input.",
        "handoff_rule": "Use the user-authorized OpenAI API fallback through scripts/image_gen.py.",
    }
    entry = next(item for item in jobs["slides"] if item["number"] == slide)
    entry.update(status="pending", blocker=None, dispatch=None, result=None)
    jobs["run_status"] = "jobs_prepared"
    write_json(jobs_path, jobs)

    prompt_path = DECK / f"prompts/slide_{slide:02d}.json"
    prompt = read_json(prompt_path)
    prompt["expected_backend"] = "scripts/image_gen.py (OpenAI API)"
    prompt["sample_generation_method"] = jobs["sample_generation_method"]
    write_json(prompt_path, prompt)


def record_blocker(slide: int, reason: str) -> None:
    run([
        str(RUNTIME_PYTHON), str(RECORD_BLOCKER), str(DECK),
        "--slide", f"slide_{slide:02d}", "--agent-id", "local-api-script",
        "--reason", reason,
    ])


def generate_slide(slide: int, args: argparse.Namespace) -> None:
    prompt_job = read_json(DECK / f"prompts/slide_{slide:02d}.json")
    references = prompt_job.get("input_images") or []
    if not references:
        raise RuntimeError(f"slide_{slide:02d} has no style reference")
    style_reference = Path(references[0]["path"])
    if not style_reference.is_file():
        raise FileNotFoundError(style_reference)

    output = DECK / f"origin_image/slide_{slide:02d}.png"
    if output.exists() and not args.force:
        raise FileExistsError(f"{output} already exists; use --force to regenerate it")

    if args.dry_run:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt_job["prompt"])
            prompt_file.flush()
            run(imagegen_command(args, style_reference, Path(prompt_file.name), output) + ["--dry-run"])
        return

    prepare_api_state(slide, args.model, args.size, args.quality)
    run([
        str(RUNTIME_PYTHON), str(RECORD_DISPATCH), str(DECK),
        "--slide", f"slide_{slide:02d}", "--agent-id", "local-api-script",
        "--agent-nickname", "OpenAI API", "--prompt-file", f"prompts/slide_{slide:02d}.json",
    ])
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt_job["prompt"])
            prompt_file.flush()
            run(imagegen_command(args, style_reference, Path(prompt_file.name), output))
        if output.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise RuntimeError(f"ImageGen did not produce a valid PNG: {output}")
        run([
            str(RUNTIME_PYTHON), str(RECORD_RESULT), str(DECK),
            "--slide", f"slide_{slide:02d}", "--agent-id", "local-api-script",
            "--backend-used", "scripts/image_gen.py (OpenAI API)",
            "--selected-source", str(output),
            "--qa-note", "Generated through the OpenAI API; PNG signature verified. Visual review remains required.",
        ])
    except Exception as error:
        record_blocker(slide, str(error))
        raise


def imagegen_command(
    args: argparse.Namespace, style_reference: Path, prompt_file: Path, output: Path
) -> list[str]:
    command = [
        str(RUNTIME_PYTHON), str(IMAGEGEN), "edit",
        "--model", args.model,
        "--image", str(style_reference),
        "--prompt-file", str(prompt_file),
        "--size", args.size,
        "--quality", args.quality,
        "--output-format", "png",
        "--no-augment",
        "--out", str(output),
    ]
    if args.force:
        command.append("--force")
    return command


def slide_articles() -> str:
    spec = read_json(DECK / "deck_spec.json")
    articles = []
    for slide in spec["slides"]:
        number = slide["number"]
        src = f"../slides/lesson-29/origin_image/slide_{number:02d}.png"
        alt = html.escape(f"{number:02d}. {slide['title']}. " + " ".join(slide["key_points"]), quote=True)
        loading = ' loading="lazy"' if number > 1 else ""
        articles.append(
            f'<article class="web-slide" data-slide-src="{src}">'
            f'<img class="web-slide-image" src="{src}" alt="{alt}"{loading}>'
            '<div class="slide-actions no-print"><button type="button" data-copy-slide>'
            'Copy slide as image</button>'
            f'<a href="{src}" download>Download PNG</a>'
            '<span data-copy-status aria-live="polite"></span></div></article>'
        )
    return "\n".join(articles) + "\n"


def finalize_lesson() -> None:
    images = sorted((DECK / "origin_image").glob("slide_*.png"))
    expected = [f"slide_{number:02d}.png" for number in range(1, 13)]
    if [path.name for path in images] != expected:
        return

    lesson_path = ROOT / "lessons/0029-resource-resolver-identity.html"
    lesson = lesson_path.read_text(encoding="utf-8")
    replacement = (
        '<h2 id="slide-deck">Complete slide deck</h2>\n'
        '<p>Copy each complete numbered image to PowerPoint or download its PNG.</p>\n'
        '<aside class="callout" lang="es"><strong>Material de la sesión 29:</strong> '
        '<a href="../reference/session-29-study-guide.html">Resumen completo en español</a> · '
        '<a href="../reference/session-29-study-guide.md" download>Markdown</a> · '
        '<a href="#ejemplos-locales">Ejemplo local</a>.</aside>\n'
        '<div class="web-deck">' + slide_articles() + '</div>'
    )
    lesson, count = re.subn(
        r'(?s)<h2 id="slide-deck">.*?</div>(?=<section id="ejemplos-locales")',
        replacement,
        lesson,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not find the Session 29 slide-deck block")
    write_text(lesson_path, lesson)

    index_path = ROOT / "index.html"
    index = index_path.read_text(encoding="utf-8").replace(
        "Guía completa, ejemplo Java, mapping de subservice y tres slides preliminares sobre identidad y ownership.",
        "Doce slides numeradas, guía completa, ejemplo Java y mapping de subservice sobre identidad y ownership.",
    )
    write_text(index_path, index)

    checker_path = ROOT / "scripts/check-session-materials.py"
    checker = checker_path.read_text(encoding="utf-8").replace(
        "[f'slide_{i:02d}.png' for i in range(1, 4)]",
        "[f'slide_{i:02d}.png' for i in range(1, 13)]",
    )
    write_text(checker_path, checker)
    run([sys.executable, str(checker_path)])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slides", type=parse_slides, default=parse_slides("4-12"))
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="2560x1440")
    parser.add_argument("--quality", choices=("low", "medium", "high", "auto"), default="high")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    required = (RUNTIME_PYTHON, IMAGEGEN, RECORD_DISPATCH, RECORD_RESULT, RECORD_BLOCKER)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        parser.error("missing Codex PPT runtime files: " + ", ".join(missing))
    if not args.dry_run and not os.getenv("OPENAI_API_KEY") and not RUNTIME_ENV.is_file():
        parser.error(
            "OPENAI_API_KEY is not configured; export it locally or configure the shared Codex PPT runtime"
        )

    for slide in args.slides:
        print(f"slide_{slide:02d}: {'checking' if args.dry_run else 'generating'}", flush=True)
        generate_slide(slide, args)
    if not args.dry_run:
        finalize_lesson()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
