#!/usr/bin/env python3
"""Gera artes sem perda, recursos versionados e CSS inline da home."""
import argparse
import hashlib
import json
import re
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
MANIFEST = OUT / 'manifest.json'
SOURCES = ('img/screen.png', 'img/screen-650.png', 'img/screen-1024.png',
           'css/acessibilidade.css', 'css/conteudos.css', 'js/mapas-responsivos.js')
ARTS = (('home-mobile', 'img/screen.png', None),
        ('home-tablet', 'img/screen-650.png', 240),
        ('home-desktop', 'img/screen-1024.png', 360))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inputs():
    return {name: digest((ROOT / name).read_bytes()) for name in SOURCES}


def dimensions(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', f'PNG inválido: {path}'
    return struct.unpack('>II', data[16:24])


def inline_css():
    css = (ROOT / 'css/acessibilidade.css').read_text()
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    return '<style id="acessibilidade-inline">' + re.sub(r'\s+', ' ', css).strip() + '</style>'


def update_html(source, resources, home=False):
    for logical, versioned in resources.items():
        stem, ext = logical.rsplit('.', 1)
        pattern = rf'(?:{re.escape(logical)}|{re.escape(stem)}\.[0-9a-f]{{12}}\.{ext})(?=[\"\'])'
        source = re.sub(pattern, versioned, source)
    for original in SOURCES[3:]:
        source = source.replace(original, resources['assets/' + Path(original).name])
    if home:
        source, count = re.subn(r'<style id="acessibilidade-inline">.*?</style>', inline_css(), source, flags=re.S)
        assert count == 1, 'Bloco de acessibilidade inline ausente na home'
    return source


def generate():
    OUT.mkdir(exist_ok=True)
    resources = {}

    def save(logical, data):
        path = Path(logical)
        versioned = f'assets/{path.stem}.{digest(data)[:12]}{path.suffix}'
        (ROOT / versioned).write_bytes(data)
        resources[logical] = versioned

    with tempfile.TemporaryDirectory(prefix='eletro-assets-') as folder:
        temp = Path(folder)
        for name, original, cut in ARTS:
            source = ROOT / original
            width, height = dimensions(source)
            parts = [(name, source)]
            if cut:
                assert height > cut, f'Arte menor que o recorte: {original}'
                parts = []
                for suffix, top, size in (('top', 0, cut), ('bottom', cut, height - cut)):
                    cropped = temp / f'{name}-{suffix}.png'
                    subprocess.run(['magick', str(source), '-crop', f'{width}x{size}+0+{top}',
                                    '+repage', '-define', 'png:exclude-chunk=date,time', str(cropped)], check=True)
                    parts.append((f'{name}-{suffix}', cropped))
            for label, png in parts:
                webp = temp / f'{label}.webp'
                subprocess.run(['cwebp', '-quiet', '-lossless', '-exact', '-z', '9', str(png), '-o', str(webp)], check=True)
                save('assets/' + label + '.png', png.read_bytes())
                save('assets/' + label + '.webp', webp.read_bytes())
    for original in SOURCES[3:]:
        save('assets/' + Path(original).name, (ROOT / original).read_bytes())
    for page in ROOT.glob('*.html'):
        before = page.read_text()
        after = update_html(before, resources, page.name == 'index.html')
        if after != before:
            page.write_text(after)
    MANIFEST.write_text(json.dumps({'inputs': inputs(), 'resources': resources}, indent=2) + '\n')
    check()


def check():
    manifest = json.loads(MANIFEST.read_text())
    assert manifest['inputs'] == inputs(), 'Fontes alteradas: execute python3 scripts/assets.py generate'
    for name in manifest['resources'].values():
        assert digest((ROOT / name).read_bytes())[:12] == Path(name).stem.rsplit('.', 1)[1], f'Recurso alterado: {name}'
    for page in ROOT.glob('*.html'):
        source = page.read_text()
        assert source == update_html(source, manifest['resources'], page.name == 'index.html'), f'{page.name}: referências/CSS inline desatualizados'
    print(f'OK: {len(manifest["resources"])} recursos versionados e CSS inline sincronizados.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('generate', 'check'))
    args = parser.parse_args()
    try:
        generate() if args.command == 'generate' else check()
    except (AssertionError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Erro: {error}\n')
