#!/usr/bin/env python3
"""Manutenção de SEO e versões textuais, sem dependências externas."""
import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://' + (ROOT / 'CNAME').read_text().strip() + '/'
NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def find(self, tag=None, **attrs):
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and all(child.attrs.get(k) == v for k, v in attrs.items()):
                    found.append(child)
                found.extend(child.find(tag, **attrs))
        return found

    def one(self, tag, **attrs):
        matches = self.find(tag, **attrs)
        if len(matches) != 1:
            raise ValueError(f'Esperado um elemento {tag} {attrs}; encontrados {len(matches)}')
        return matches[0]

    def text(self):
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
        self.feed(source)
        self.close()
        if len(self.stack) != 1:
            raise ValueError('HTML com elementos não fechados')

    def handle_starttag(self, tag, attrs):
        if len(dict(attrs)) != len(attrs):
            raise ValueError(f'Atributo duplicado em {tag}')
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if len(self.stack) < 2 or self.stack[-1].tag != tag:
            raise ValueError(f'Fechamento inesperado: {tag}')
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def read_page(path):
    return Document(path.read_text()).root


def sitemap():
    return ET.parse(ROOT / 'sitemap.xml').findall('s:url', NS)


def filename(url):
    return unquote(urlsplit(url).path).lstrip('/') or 'index.html'


def pages():
    return [(entry.find('s:loc', NS).text, read_page(ROOT / filename(entry.find('s:loc', NS).text))) for entry in sitemap()]


def graph(doc):
    return json.loads(doc.one('script', type='application/ld+json').text())['@graph']


def markdown(node, page_url):
    if isinstance(node, str):
        return re.sub(r'\s+', ' ', node)
    if node.tag in ('script', 'style', 'nav', 'img', 'map'):
        return ''
    if node.tag == 'form':
        button = node.one('button', type='submit')
        return '\n\n[' + clean(button.text()) + '](' + urljoin(page_url, node.attrs['action']) + ')\n\n'
    if node.attrs.get('class') == 'article-label':
        return ''
    if node.attrs.get('class') == 'contact-actions':
        return '\n\n' + '\n'.join('- ' + markdown(link, page_url) for link in node.find('a')) + '\n\n'
    inner = ''.join(markdown(c, page_url) for c in node.children)
    if node.tag in ('h1', 'h2', 'h3', 'h4'):
        return '\n\n' + '#' * int(node.tag[1]) + ' ' + clean(inner) + '\n\n'
    if node.tag == 'p':
        return '\n\n' + clean(inner) + '\n\n'
    if node.tag == 'a':
        return f'[{clean(inner)}]({urljoin(page_url, node.attrs["href"])})'
    if node.tag in ('strong', 'b'):
        return '**' + inner.strip() + '**'
    if node.tag in ('em', 'i'):
        return '*' + inner.strip() + '*'
    if node.tag in ('ul', 'ol'):
        items = [c for c in node.children if isinstance(c, Node) and c.tag == 'li']
        lines = []
        for i, item in enumerate(items, 1):
            prefix = f'{i}. ' if node.tag == 'ol' else '- '
            content = ''.join(markdown(c, page_url) for c in item.children).strip()
            # O índice usa h3 dentro dos itens; preservar os títulos como seções.
            lines.append(content if item.find('h3') else prefix + clean(content))
        return '\n\n' + '\n\n'.join(lines) + '\n\n'
    if node.tag == 'table':
        rows = []
        for row in node.find('tr'):
            cells = [c for c in row.children if isinstance(c, Node) and c.tag in ('th', 'td')]
            rows.append('| ' + ' | '.join(clean(markdown(c, page_url)).replace('|', '\\|') for c in cells) + ' |')
        if rows:
            columns = len(node.find('tr')[0].find('th')) or len(node.find('tr')[0].find('td'))
            rows.insert(1, '| ' + ' | '.join(['---'] * columns) + ' |')
        caption = node.find('caption')
        return '\n\n' + (clean(caption[0].text()) + '\n\n' if caption else '') + '\n'.join(rows) + '\n\n'
    return inner


def generated_files():
    entries = pages()
    result = {}
    for url, doc in entries:
        content = markdown(doc.one('main'), url)
        for contact in doc.find('section', **{'class': 'contact-section'}):
            content += markdown(contact, url)
        text = 'Fonte canônica: ' + url + '\n\n' + content.strip()
        result[filename(url) + '.md'] = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', text).strip() + '\n'
    home = next(doc for url, doc in entries if url == BASE)
    org = next(n for n in graph(home) if n['@type'] == 'Organization')
    lines = [f'# {org["name"]}', '', '> ' + org['description'], '',
             f'Telefone e WhatsApp: {org["telephone"]}.',
             'Atendimento exclusivamente no local do cliente. Não há endereço fixo para receber clientes ou equipamentos.',
             'A visita e o orçamento são gratuitos. A execução dos serviços e as peças têm valor próprio, apresentado após a avaliação.']
    if org.get('slogan'):
        lines += ['', org['slogan']]
    lines += ['', '## Atendimento e conteúdos', '']
    for url, doc in entries:
        title = clean(doc.one('h1').text())
        description = doc.one('meta', name='description').attrs['content']
        lines.append(f'- [{title}]({BASE}{filename(url)}.md): {description}')
    lines += ['', '## Perfis oficiais', '']
    for url in org['sameAs']:
        label = 'Facebook' if 'facebook.com' in url else 'Perfil da Empresa no Google'
        lines.append(f'- [{label}]({url})')
    result['llms.txt'] = '\n'.join(lines) + '\n'
    return result


def generate():
    outputs = generated_files()
    for name, content in outputs.items():
        (ROOT / name).write_text(content)
    print(f'Gerados {len(outputs)} arquivos a partir dos HTMLs. O sitemap e suas datas não foram alterados.')


def check():
    entries = pages()
    urls = [url for url, _ in entries]
    assert len(urls) == len(set(urls)), 'URL duplicada no sitemap'
    expected = {BASE + ('' if p.name == 'index.html' else p.name) for p in ROOT.glob('*.html') if p.name != '404.html'}
    assert set(urls) == expected, 'Sitemap e páginas HTML não correspondem'
    docs = {filename(url): doc for url, doc in entries}
    docs['404.html'] = read_page(ROOT / '404.html')
    titles, descriptions = set(), set()
    edges = {name: set() for name in docs}
    count = 0
    for name, doc in docs.items():
        doc.one('main'); doc.one('h1')
        assert doc.one('html').attrs.get('lang') == 'pt-BR', f'{name}: idioma ausente'
        viewport = doc.one('meta', name='viewport').attrs['content'].replace(' ', '')
        assert 'user-scalable=no' not in viewport and 'maximum-scale=1' not in viewport, f'{name}: zoom restrito'
        ids = [n.attrs['id'] for n in doc.find() if 'id' in n.attrs]
        assert len(ids) == len(set(ids)), f'{name}: IDs duplicados'
        skips = doc.find('a', **{'class': 'skip-link'})
        assert skips, f'{name}: atalho de navegação ausente'
        for skip in skips:
            target = skip.attrs.get('href', '')
            if target.startswith('#'):
                destination = doc.one(None, id=target[1:])
                assert destination.attrs.get('tabindex') == '-1', f'{name}: destino do atalho não recebe foco'
        previous_level = 0
        for heading in (n for n in doc.find() if re.fullmatch(r'h[1-6]', n.tag)):
            level = int(heading.tag[1])
            assert level <= previous_level + 1, f'{name}: salto na hierarquia de títulos'
            previous_level = level
        for hidden in doc.find(**{'class': 'visually-hidden'}):
            assert not hidden.find('a') and not hidden.find('button'), f'{name}: controle visualmente oculto'
        for field in doc.find('textarea') + doc.find('input'):
            if field.attrs.get('type') != 'hidden':
                assert doc.find('label', **{'for': field.attrs.get('id')}), f'{name}: campo sem rótulo'
        for table in doc.find('table'):
            table.one('caption')
            assert table.find('th'), f'{name}: tabela sem cabeçalhos'
            assert all(th.attrs.get('scope') in ('col', 'row', 'colgroup', 'rowgroup') for th in table.find('th'))
        for node in doc.find():
            assert int(node.attrs.get('tabindex', '-1')) <= 0, f'{name}: ordem artificial de foco'
            for attr in ('href', 'src', 'action'):
                if attr not in node.attrs:
                    continue
                url = urlsplit(urljoin(BASE + name, node.attrs[attr]))
                if url.scheme != 'https' or url.netloc != urlsplit(BASE).netloc:
                    continue
                target = filename(url.geturl())
                assert (ROOT / target).is_file(), f'{name}: referência inexistente {target}'
                if url.fragment and target in docs:
                    assert docs[target].find(id=unquote(url.fragment)), f'{name}: âncora inválida {url.fragment}'
                if node.tag == 'a' and target in docs:
                    edges[name].add(target)
                count += 1
            if node.tag == 'area':
                assert node.attrs.get('alt'), f'{name}: mapa sem descrição acessível'
            if node.tag == 'img':
                assert 'alt' in node.attrs, f'{name}: imagem sem atributo alt'
                if 'usemap' in node.attrs:
                    assert node.attrs['alt'], f'{name}: contexto do mapa ausente'
                    assert doc.find('map', name=node.attrs['usemap'].lstrip('#'))
            if node.attrs.get('target') == '_blank':
                label = node.attrs.get('alt', '') + node.text()
                assert 'nova aba' in label, f'{name}: abertura de aba sem aviso'
                assert 'noopener' in node.attrs.get('rel', '').split()
            for attr in ('aria-labelledby', 'aria-describedby'):
                for ref in node.attrs.get(attr, '').split():
                    assert ref in ids, f'{name}: {attr} inexistente'
        if name == '404.html':
            assert 'noindex' in doc.one('meta', name='robots').attrs['content']
            continue
        title = doc.one('title').text()
        description = doc.one('meta', name='description').attrs['content']
        assert title not in titles and description not in descriptions, 'Metadados duplicados'
        titles.add(title); descriptions.add(description)
        canonical = BASE + ('' if name == 'index.html' else name)
        assert doc.one('link', rel='canonical').attrs['href'] == canonical
        for prop, value in [('og:url', canonical), ('og:title', title), ('og:description', description)]:
            assert doc.one('meta', property=prop).attrs['content'] == value
        data = graph(doc)
        known_ids = {n['@id'] for n in data}
        def refs(value):
            if isinstance(value, dict):
                if set(value) == {'@id'}:
                    assert value['@id'] in known_ids, f'{name}: entidade sem definição'
                for child in value.values(): refs(child)
            elif isinstance(value, list):
                for child in value: refs(child)
        refs(data)
        page = next(n for n in data if n['@type'] in ('WebPage', 'CollectionPage'))
        assert page['url'] == canonical and page['name'] == title
        assert page['description'] == description
    reached, todo = set(), ['index.html']
    while todo:
        name = todo.pop()
        if name not in reached:
            reached.add(name); todo.extend(edges[name] - reached)
    assert set(docs) - {'404.html'} <= reached, 'Página sem caminho de navegação'
    css = ''.join(p.read_text() for p in (ROOT / 'css').glob('*.css')) + docs['index.html'].one('style').text()
    for target in re.findall(r'url\([\'"]?([^\)\'\"]+)', css):
        assert (ROOT / target).exists(), f'Arquivo do CSS inexistente: {target}'
    for entry in sitemap():
        lastmod = entry.find('s:lastmod', NS)
        if lastmod is not None:
            date.fromisoformat(lastmod.text)
    robots = RobotFileParser()
    robots.parse((ROOT / 'robots.txt').read_text().splitlines())
    for bot in ('Googlebot', 'Bingbot', 'OAI-SearchBot', 'PerplexityBot', 'Claude-SearchBot'):
        assert all(robots.can_fetch(bot, url) for url in urls), f'Rastreamento bloqueado: {bot}'
    for name, content in generated_files().items():
        assert (ROOT / name).read_text() == content, f'{name} desatualizado; execute generate'
    print(f'OK: {len(docs)} HTMLs, {len(urls)} URLs indexáveis e {count} referências locais.')
    print('OK: navegação, âncoras, metadados, JSON-LD, arquivos do CSS, robots e versões textuais.')
    print('OK: idioma, zoom permitido, atalhos, títulos, rótulos, mapas e referências acessíveis.')


def indexnow(submit):
    key = (ROOT / 'indexnow-key.txt').read_text().strip()
    assert re.fullmatch(r'[a-zA-Z0-9-]{8,128}', key), 'Chave IndexNow inválida'
    entries = pages()
    payload = {'host': urlsplit(BASE).netloc, 'key': key, 'keyLocation': BASE + 'indexnow-key.txt', 'urlList': [url for url, _ in entries]}
    if not submit:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print('Simulação: nada enviado. Após publicar, use indexnow --submit.')
        return
    with urlopen(BASE + 'indexnow-key.txt', timeout=20) as response:
        assert response.read().decode().strip() == key, 'A chave local ainda não está publicada'
    for url, local in entries:
        with urlopen(url, timeout=20) as response:
            assert response.status == 200 and response.url == url, f'URL publicada diverge: {url}'
            remote = Document(response.read().decode('utf-8')).root
        assert remote.one('link', rel='canonical').attrs['href'] == url
        assert clean(remote.one('main').text()) == clean(local.one('main').text()), f'Conteúdo ainda não publicado: {url}'
    request = Request('https://api.indexnow.org/indexnow', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    with urlopen(request, timeout=30) as response:
        print(f'IndexNow respondeu HTTP {response.status}. Recebimento não garante indexação.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('generate', help='Atualiza llms.txt e Markdown a partir dos HTMLs')
    sub.add_parser('check', help='Valida o site local e as versões textuais')
    notify = sub.add_parser('indexnow', help='Simula a notificação de URLs publicadas')
    notify.add_argument('--submit', action='store_true', help='Confere a publicação e envia as URLs ao IndexNow')
    args = parser.parse_args()
    try:
        if args.command == 'generate': generate()
        elif args.command == 'check': check()
        else: indexnow(args.submit)
    except (AssertionError, ValueError, OSError, HTTPError, URLError, ET.ParseError) as error:
        print(f'Erro: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
