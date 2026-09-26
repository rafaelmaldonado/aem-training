"""Check sessions 18–24, 26–29 and 31–33: links, slides and source consistency."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.blocks = [], [], []
        self.in_pre = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ('href', 'src'):
            if attr in attrs:
                self.links.append(attrs[attr])
        if tag == 'pre':
            self.in_pre = True
            self.blocks.append('')

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.in_pre = False

    def handle_data(self, data):
        if self.in_pre:
            self.blocks[-1] += data


pages = [ROOT / 'index.html', ROOT / 'reference/index.html']
for session in (*range(18, 25), 26, 27, 28, 29, 31, 32, 33):
    lesson = list((ROOT / 'lessons').glob(f'{session:04d}-*.html'))
    assert len(lesson) == 1, (session, lesson)
    pages += lesson + [ROOT / f'reference/session-{session}-study-guide.html']

for path in pages:
    page = Page(path)
    assert len(page.ids) == len(set(page.ids)), f'Duplicate id: {path}'
    if path not in pages[:2]:
        anchor = 'ejemplos-locales' if path.name.startswith(('0023-', 'session-23-', '0024-', 'session-24-', '0026-', 'session-26-', '0027-', 'session-27-', '0028-', 'session-28-', '0029-', 'session-29-', '0031-', 'session-31-', '0032-', 'session-32-', '0033-', 'session-33-')) else 'practica-local'
        assert anchor in page.ids, f'Missing example anchor: {path}'
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.exists(), f'Broken link: {path}: {link}'
        if url.fragment and target.suffix == '.html':
            assert unquote(url.fragment) in Page(target).ids, f'Broken anchor: {path}: {link}'

for session in (18, 19, 22, 23, 26, 27, 28, 29):
    lab = ROOT / f'reference/examples/session-{session}'
    lesson = next((ROOT / 'lessons').glob(f'{session:04d}-*.html'))
    guide = ROOT / f'reference/session-{session}-study-guide.html'
    for source in lab.rglob('*'):
        if not source.is_file():
            continue
        if source.name == 'README.md':
            continue
        if source.suffix == '.xml':
            ET.parse(source)
        if source.suffix == '.json':
            json.loads(source.read_text())
        for target in (lesson, guide):
            assert source.read_text().strip() in [b.strip() for b in Page(target).blocks], (source, target)

lab = ROOT / 'reference/examples/session-28'
config = json.loads(next(lab.rglob('*.cfg.json')).read_text())
assert config['scripts'] == [(lab / 'permissions.repoinit').read_text()], 'Repo Init JSON differs from readable source'

slide_count = 0
for session in (22, 23, 24, 26, 27, 28, 31, 32, 33):
    images = sorted((ROOT / f'slides/lesson-{session}/origin_image').glob('*.png'))
    assert [p.name for p in images] == [f'slide_{i:02d}.png' for i in range(1, 13)]
    slide_count += len(images)
    for image in images:
        assert image.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n', image
    lesson = next((ROOT / 'lessons').glob(f'{session:04d}-*.html'))
    assert 'speech' not in lesson.read_text().lower()
    assert not (ROOT / f'slides/lesson-{session}/speech.md').exists()

session_29_images = sorted((ROOT / 'slides/lesson-29/origin_image').glob('*.png'))
assert [p.name for p in session_29_images] == [f'slide_{i:02d}.png' for i in range(1, 13)]
for image in session_29_images:
    assert image.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n', image
slide_count += len(session_29_images)
assert not (ROOT / 'slides/lesson-29/speech.md').exists()
print(f'OK: {len(pages)} HTML pages, {slide_count} PNG slides, local links, example anchors, XML/JSON and literal source blocks.')
