"""Rebuild the standalone Chinese EPUB and verify its packaged navigation."""
from pathlib import Path
import json
import re
import subprocess
import zipfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit
import posixpath

root = Path(__file__).resolve().parent
stem = 'DeepSeek-Harness-小白入门'
subprocess.run([
    'pandoc', str(root / (stem + '.txt')), '--from=markdown', '--to=epub3',
    '--toc', '--toc-depth=2', '--split-level=1',
    '--epub-cover-image=' + str(root / 'cover.svg'),
    '--css=' + str(root / 'reading.css'),
    '--output=' + str(root / (stem + '.epub')),
], check=True)
ns = {'o': 'http://www.idpf.org/2007/opf',
      'x': 'http://www.w3.org/1999/xhtml',
      'd': 'http://purl.org/dc/elements/1.1/'}
with zipfile.ZipFile(root / (stem + '.epub')) as z:
    assert z.testzip() is None, 'ZIP corruption'
    first = z.infolist()[0]
    assert first.filename == 'mimetype' and first.compress_type == zipfile.ZIP_STORED
    assert z.read('mimetype') == b'application/epub+zip'
    container = ET.fromstring(z.read('META-INF/container.xml'))
    opf_path = next(e.attrib['full-path'] for e in container.iter() if e.tag.endswith('rootfile'))
    opf = ET.fromstring(z.read(opf_path))
    assert opf.attrib['version'] == '3.0'
    assert opf.find('o:metadata/d:language', ns).text == 'zh-CN'
    manifest = {e.attrib['id']: e.attrib for e in opf.findall('o:manifest/o:item', ns)}
    base = posixpath.dirname(opf_path)
    for entry in manifest.values():
        assert posixpath.normpath(posixpath.join(base, unquote(entry['href']))) in z.namelist()
    assert any('cover-image' in e.get('properties', '').split() for e in manifest.values())
    xmls = {name: ET.fromstring(z.read(name)) for name in z.namelist()
            if name.endswith(('.xhtml', '.svg', '.opf', '.ncx', '.xml'))}
    for name, tree in xmls.items():
        for element in tree.iter():
            for attr in ('href', 'src'):
                value = element.get(attr)
                if not value:
                    continue
                parsed = urlsplit(value)
                if parsed.scheme or parsed.netloc:
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(parsed.path))) if parsed.path else name
                assert target in z.namelist(), (name, value)
                if parsed.fragment:
                    assert target in xmls
                    assert any(e.get('id') == unquote(parsed.fragment) for e in xmls[target].iter()), (name, value)
    nav = next(e for e in manifest.values() if 'nav' in e.get('properties', '').split())
    navtree = xmls[posixpath.join(base, nav['href'])]
    labels = [''.join(e.itertext()).strip() for e in navtree.findall('.//x:a', ns)]
    source = (root / (stem + '.txt')).read_text()
    headings = re.findall(r'^# (.+)$', source, re.M)
    for heading in headings:
        assert heading in labels, heading
    spine = [e.attrib['idref'] for e in opf.findall('o:spine/o:itemref', ns)]
    spine_text = '\n'.join(''.join(xmls[posixpath.join(base, manifest[key]['href'])].itertext()) for key in spine)
    for heading in headings:
        assert heading in spine_text
    assert '第十二章' in spine_text and '参考要点' in spine_text
    assert 'TODO' not in source and '待补' not in source
    report = {'format': 'EPUB 3', 'title': opf.find('o:metadata/d:title', ns).text,
              'language': 'zh-CN', 'main_chapters': 12,
              'top_level_sections': len(headings), 'navigation_links': len(labels),
              'chinese_characters_in_source': len(re.findall(r'[\u4e00-\u9fff]', source)),
              'size_bytes': (root / (stem + '.epub')).stat().st_size,
              'checks': ['ZIP integrity and mimetype', 'XML parsing', 'manifest resources',
                         'local links and fragment targets', 'cover declaration',
                         'all chapters in navigation and reading order'],
              'limitations': ['EPUBCheck not run: Java runtime unavailable',
                              'Application launch and real model API not exercised']}
(root / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
