"""Check sessions 18–23: links, slide assets and copyable source consistency."""
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
for session in range(18, 24):
    lesson = list((ROOT / 'lessons').glob(f'{session:04d}-*.html'))
    assert len(lesson) == 1, (session, lesson)
    pages += lesson + [ROOT / f'reference/session-{session}-study-guide.html']

for path in pages:
    page = Page(path)
    assert len(page.ids) == len(set(page.ids)), f'Duplicate id: {path}'
    if path not in pages[:2]:
        anchor = 'ejemplos-locales' if path.name.startswith(('0023-', 'session-23-')) else 'practica-local'
        assert anchor in page.ids, f'Missing example anchor: {path}'
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.exists(), f'Broken link: {path}: {link}'
        if url.fragment and target.suffix == '.html':
            assert unquote(url.fragment) in Page(target).ids, f'Broken anchor: {path}: {link}'

for session in (18, 19, 22, 23):
    lab = ROOT / f'reference/examples/session-{session}'
    lesson = next((ROOT / 'lessons').glob(f'{session:04d}-*.html'))
    guide = ROOT / f'reference/session-{session}-study-guide.html'
    for source in lab.rglob('*'):
        if not source.is_file():
            continue
        if source.suffix == '.xml':
            ET.parse(source)
        if source.suffix == '.json':
            json.loads(source.read_text())
        for target in (lesson, guide):
            assert source.read_text().strip() in [b.strip() for b in Page(target).blocks], (source, target)

for session in (22, 23):
    images = sorted((ROOT / f'slides/lesson-{session}/origin_image').glob('*.png'))
    assert [p.name for p in images] == [f'slide_{i:02d}.png' for i in range(1, 13)]
    for image in images:
        assert image.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n', image
    lesson = next((ROOT / 'lessons').glob(f'{session:04d}-*.html'))
    assert 'speech' not in lesson.read_text().lower()
    assert not (ROOT / f'slides/lesson-{session}/speech.md').exists()
print(f'OK: {len(pages)} HTML pages, 24 PNG slides, local links, example anchors, XML/JSON and literal source blocks.')
