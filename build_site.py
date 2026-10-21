"""Generate a dependency-free reading site from the Chinese manuscript."""
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parent
site = root / 'docs'
site.mkdir(exist_ok=True)
body = subprocess.check_output([
    'pandoc', str(root / 'DeepSeek-Harness-小白入门.txt'), '--from=markdown',
    '--to=html5', '--standalone', '--toc', '--toc-depth=2',
    '--metadata=pagetitle:从零认识 DeepSeek Harness',
    '--template=' + str(root / 'site-template.html'),
], text=True)
(site / 'index.html').write_text(body)
for source, target in [('site.css', 'site.css'), ('reader.js', 'reader.js'), ('cover.svg', 'cover.svg'),
                       ('DeepSeek-Harness-小白入门.epub', 'deepseek-harness-book.epub')]:
    shutil.copyfile(root / source, site / target)
(site / '.nojekyll').touch()
print('Built docs/index.html and offline assets.')
