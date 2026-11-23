# Eletro Assistec Coelho

Site estático de assistência técnica para máquinas de lavar convencionais, lava e seca e secadoras em Balneário Camboriú, SC.

## Página inicial

`index.html` mantém as artes, dimensões, coordenadas dos mapas e identidade visual. Os acréscimos incluem metadados de SEO, dados estruturados, links de conteúdo e melhorias no acesso ao contato. O formulário conserva o envio GET para o WhatsApp e recebeu instruções, contraste e controles maiores. As áreas clicáveis têm descrições acessíveis.

As imagens `img/screen.png`, `img/screen-650.png` e `img/screen-1024.png` são as fontes das artes. Os fundos de tablet e desktop possuem versões WebP sem perda de pixels, selecionadas por `image-set`, com fallback PNG. O arquivo mobile e as imagens transparentes dos mapas foram preservados. As cópias com sufixos de backup não são referenciadas pelo HTML.

Depois de editar as artes no Canva, atualize as variantes WebP; caso contrário, navegadores modernos continuarão mostrando a arte anterior. Mantenha o conteúdo dos três tamanhos consistente com os serviços atuais. Ao mudar posições ou dimensões, confira as coordenadas dos mapas clicáveis.

```sh
cwebp -quiet -lossless -exact -z 9 img/screen-650.png -o img/screen-650.webp
cwebp -quiet -lossless -exact -z 9 img/screen-1024.png -o img/screen-1024.webp
```

## Páginas internas

Os conteúdos são organizados por dúvidas e situações, sem separar máquinas de lavar e lava e seca em páginas de catálogo:

- `servicos.html`: apresentação da empresa, serviços, equipamentos, marcas e compromisso com o cliente.
- `duvidas-e-orientacoes.html`: índice de oito conteúdos, organizado por sintomas, cuidados e dúvidas sobre o atendimento.
- `manutencao-e-higienizacao.html`: manutenção preventiva e corretiva, limpeza e higienização.
- `instalacao-de-lavadoras-e-secadoras.html`: instalação, reinstalação e informações para organizar a visita.
- `reparo-de-placas-e-pecas.html`: reparo de placas eletrônicas, troca de peças danificadas e perguntas sobre o serviço proposto.
- `maquina-nao-escoa-agua.html`: água parada no tambor, observações sobre drenagem e informações para solicitar atendimento.
- `maquina-nao-centrifuga.html`: o que observar quando a centrifugação não acontece como esperado.
- `lava-e-seca-nao-seca.html`: como descrever problemas na secagem e conferir as informações do modelo.
- `consertar-ou-trocar.html`: perguntas e critérios para comparar reparo e substituição.
- `visita-tecnica-gratuita.html`: o que é gratuito, como agendar e como funciona o atendimento no local.

Os textos estão diretamente no HTML. Os artigos incluem sumário, links relacionados, contato e metadados próprios. A navegação interna e o caminho de navegação levam ao índice de dúvidas. As orientações técnicas gerais citam fontes oficiais dos fabricantes; não substituem o manual específico ou a avaliação do equipamento.

`css/conteudos.css` usa seletores isolados: `.content-page` nas páginas internas e `.home-content-links` nos links do rodapé da home. Não substitui os estilos da página inicial. Nenhuma nova biblioteca JavaScript é necessária para os conteúdos.

`css/acessibilidade.css` é carregado por último nas doze páginas HTML, incluindo a página 404. Reúne os ajustes de foco, contraste, tamanho dos controles e preferências de exibição. As mudanças são feitas no HTML e no CSS, sem uma nova dependência JavaScript.

## Dados da empresa

- WhatsApp e telefone: `(47) 99675-9575`.
- Área de atendimento: Balneário Camboriú, SC.
- Atendimento exclusivamente no local, sem endereço fixo para receber clientes.
- Visita e orçamento gratuitos; o valor do reparo é apresentado após a avaliação.
- Perfil no Google: `https://share.google/2EQlhfNVgxlwBOWjh`.
- Marcas atendidas: LG, Samsung, Midea, Brastemp, Consul e Electrolux.
- Equipamentos: máquinas de lavar convencionais, lava e seca e secadoras.
- Serviços: manutenção preventiva e corretiva, instalação, limpeza e higienização, troca de peças danificadas e reparo de placas eletrônicas.
- Slogan: “Qualidade e confiança em cada serviço!”.

Horários, prazos de garantia e credenciamento por fabricante não foram informados. Não há promessas de conclusão do reparo no mesmo dia.

## Mensagem e personalidade da empresa

“Assistência técnica especializada” é uma mensagem central da marca e deve permanecer nas apresentações da empresa, nas chamadas de contato, nos metadados principais e na descrição estruturada. Ao ampliar os serviços ou revisar os textos, preservar essa expressão junto de agilidade, qualidade e confiança.

O escopo acima foi confirmado pela descrição do Perfil da Empresa fornecida pelo proprietário em 2026-11-23. O texto anterior do site se concentrava em conserto, sintomas e visita gratuita. Secadoras e os demais serviços passaram a ter presença explícita nos textos visíveis, navegação, metadados e arquivos para agentes.

| Informação da descrição fornecida | Onde aparece no site |
| --- | --- |
| Especialização em lavadoras convencionais, lava e seca e secadoras | Home, `servicos.html`, visita e novas páginas de serviços |
| LG, Samsung, Midea, Brastemp, Consul e Electrolux | Apresentação dos serviços, visita, novos conteúdos e descrição estruturada da empresa |
| Manutenção preventiva e corretiva | `manutencao-e-higienizacao.html` |
| Limpeza e higienização | `manutencao-e-higienizacao.html` |
| Instalação | `instalacao-de-lavadoras-e-secadoras.html` |
| Troca de peças danificadas e reparo de placas eletrônicas | `reparo-de-placas-e-pecas.html` |
| Agilidade, qualidade, confiança e atendimento profissional | Apresentação da empresa, chamadas de contato e textos dos serviços |
| Bom funcionamento, durabilidade e satisfação do cliente | Compromissos da empresa na página de serviços, sem estimativas ou garantias de resultado não informadas |
| “Qualidade e confiança em cada serviço!” | Página de serviços, rodapés internos, `Organization.slogan` e `llms.txt` |

A voz dos textos é profissional, direta e próxima: explica como a equipe pode ajudar e o que o cliente precisa saber para decidir. Evitar superlativos sem comprovação, afirmação de assistência autorizada, promessa de peças originais ou garantia com prazo não confirmado. O escopo técnico dos serviços foi informado pelo proprietário; não foram inventados casos reais, certificações ou resultados de reparos.

## Manutenção e SEO

O site não precisa de build. Edite os HTMLs diretamente. Ao mudar telefone ou dados da empresa, atualize também os metadados e os blocos JSON-LD de todas as páginas.

O sitemap contém onze URLs: a home, a apresentação dos serviços, o índice de dúvidas e oito conteúdos. Ao adicionar páginas, inclua links de navegação e atualize `sitemap.xml`. O `robots.txt` permite o rastreamento e aponta para o sitemap. Depois da publicação, confira a versão entregue pela Cloudflare e envie o sitemap aos mecanismos de busca.

Os dados estruturados identificam a empresa como `Organization`, sem inventar endereço comercial, e relacionam as páginas ao `WebSite`. A cidade está associada a Santa Catarina e ao Brasil, e o contato identifica o atendimento ao cliente em português. A descrição e o slogan da empresa são consistentes em todas as páginas. A home descreve o conjunto de serviços de assistência técnica. Os artigos incluem `WebPage` e `BreadcrumbList`; o índice usa `CollectionPage` com uma `ItemList` dos oito assuntos. Não há avaliações ou datas de publicação artificiais. Cada página tem URL canônica e metadados de compartilhamento próprios.

O identificador Google Ads existente, `AW-932054382`, foi preservado. Não foram criados identificadores de Analytics nem rótulos de conversão.

Para visualizar, use o servidor de sua preferência na raiz do projeto. A configuração de Live Preview do VS Code aponta para `index.html`.

## SEO, AEO e GEO

- **SEO:** páginas rastreáveis, links internos, metadados, sitemap, dados estruturados coerentes e carregamento das artes.
- **AEO:** perguntas com respostas diretas e visíveis, especialmente sobre atendimento e orçamento. Os textos técnicos apresentam observações, fontes e limites do diagnóstico remoto.
- **GEO:** identificação consistente da empresa, fatos verificáveis, fontes e acesso ao conteúdo. `llms.txt` é um complemento para agentes que o utilizem, sem promessa de posicionamento ou citação.

O Google informa que `llms.txt` não melhora nem prejudica o posicionamento na busca ou nos seus recursos de IA. Não há marcação especial que garanta presença em respostas geradas. Não foram criadas avaliações, credenciais, casos de sucesso ou páginas repetidas por bairros. Casos reais e fotos próprias podem enriquecer os conteúdos quando estiverem disponíveis.

### Arquivos para agentes

`llms.txt` contém um resumo da empresa, serviços, marcas, slogan e um índice das onze versões `*.html.md`. Cada versão textual deriva do HTML correspondente, mantém as fontes e informa a URL canônica. Os HTMLs apontam para essas versões por `rel="alternate"` e para o índice por `rel="describedby"`. O sitemap lista somente as páginas HTML canônicas.

O arquivo vazio `.nojekyll` mantém a publicação estática no GitHub Pages, evitando que o Jekyll transforme os arquivos Markdown. Ele precisa estar na raiz da pasta publicada, junto de `index.html` e `CNAME`. Os scripts Python são ferramentas locais de manutenção, não código executado pelo servidor.

Depois de editar os HTMLs, execute:

```sh
python3 scripts/seo.py generate
python3 scripts/seo.py check
```

O gerador não altera os HTMLs, o sitemap ou as datas. O verificador confere navegação, âncoras, referências locais, JSON-LD, metadados, arquivos usados pelo CSS, permissões do robots e sincronização das versões textuais. Também verifica idioma, zoom permitido, destinos dos atalhos, hierarquia dos títulos, rótulos, descrições dos mapas e referências ARIA. Ele não sobe um servidor nem publica arquivos.

O `lastmod` do sitemap corresponde à alteração relevante do conteúdo ou dos metadados, não à data de cada execução. Atualize apenas a entrada da página efetivamente alterada. As onze entradas refletem as alterações de conteúdo e dados estruturados em 2026-11-23.

### IndexNow após publicar

`indexnow-key.txt` contém a chave pública de comprovação do domínio para o protocolo IndexNow. Não é uma senha de conta. O arquivo deve ser publicado junto com o site. A integração está preparada, mas nenhuma URL foi enviada nesta implementação.

```sh
# Mostra a solicitação sem enviar nada:
python3 scripts/seo.py indexnow

# Depois de publicar o site e a chave:
python3 scripts/seo.py indexnow --submit
```

Antes do envio, o comando confere a chave publicada, o status HTTP, a URL canônica e o conteúdo principal das páginas listadas no sitemap. Só então notifica `api.indexnow.org`. O recebimento não garante indexação nem posicionamento. Não execute no navegador do visitante; use após uma publicação relevante. Para este site estático, a integração é manual e pode ser ligada ao fluxo de publicação posteriormente.

### Conferências na hospedagem e nos buscadores

Estas etapas dependem do domínio publicado e das contas externas; não foram executadas pelo script local:

1. Confirmar no Google Search Console e no Bing Webmaster Tools o acesso ao domínio, enviar o sitemap e verificar a indexação das onze URLs. A verificação pode ser feita por DNS ou pelo arquivo/meta fornecido por cada serviço; não criar tokens fictícios.
2. Conferir se HTTP e `www` redirecionam para `https://eletroassisteccoelho.com.br/`, preservando o caminho. Conferir também a consolidação de `/index.html` com `/`. A configuração depende da hospedagem; não há regra genérica `_redirects` ou `.htaccess` ativa neste repositório.
3. Publicar `404.html` na raiz usada pelo GitHub Pages e conferir sua resposta HTTP **404** em um caminho inexistente. Seus links absolutos funcionam mesmo em URLs aninhadas. Ela tem `noindex` e está fora do sitemap. Não redirecionar todos os erros para a home.
4. Conferir o `robots.txt` realmente entregue pela hospedagem/CDN e as regras de firewall. A regra local permite todos os robôs. `OAI-SearchBot` atende à busca do ChatGPT; `GPTBot` é um controle independente para treinamento. O `llms.txt` não concede nem revoga essas permissões.
5. Confirmar tipo de conteúdo adequado para `.md` (`text/markdown` ou `text/plain`) e `.txt` (`text/plain`). Os arquivos Markdown precisam ser servidos como texto, sem transformação em páginas HTML pela hospedagem.
6. Medir o carregamento no PageSpeed Insights após publicar. Configurar compressão de HTML/CSS/textos e cache dos recursos na hospedagem, purgando o cache ao atualizar as artes de mesmo nome.
7. Manter o Perfil da Empresa no Google como atendimento por área de serviço, sem endereço público de recepção. Conferir telefone, serviços, cidade, fotos e horários reais. Avaliações devem vir de clientes reais.
8. Acompanhar consultas, páginas indexadas, visitas e contatos. O identificador existente de Google Ads não define sozinho eventos de conversão. Para medir WhatsApp e ligações, usar os identificadores de medição/conversão da conta antes de configurar eventos; cliques não equivalem a reparos contratados.

### Situação pública observada em 2026-11-23

As respostas públicas indicam **GitHub Pages atrás da Cloudflare**: os cabeçalhos identificam Cloudflare e o corpo da página 404 identifica GitHub Pages. O repositório configurado localmente é `dearaujowine/eletroassisteccoelho` no GitHub. Isso não confirma a branch ou pasta selecionada para publicação; conferir em Settings → Pages.

| URL | Resultado com requisição GET de navegador |
| --- | --- |
| `https://eletroassisteccoelho.com.br/` | HTTP 200 |
| `http://eletroassisteccoelho.com.br/` | Redireciona para HTTPS, com resposta final 200 |
| `https://www.eletroassisteccoelho.com.br/` | Redireciona para o domínio sem `www`, com resposta final 200 |
| `/index.html` | HTTP 200, sem redirecionar para `/` |
| `/robots.txt` | HTTP 200, contendo somente comentários de sinais de conteúdo; sem a declaração local do sitemap |
| `/sitemap.xml` | HTTP 404, página de erro do GitHub Pages |
| `/duvidas-e-orientacoes.html` | HTTP 404 |

Requisições HEAD automatizadas receberam HTTP 403; requisições GET com identificação de navegador conseguiram acessar a home e o robots. Isso não prova bloqueio do Googlebot ou do OAI-SearchBot. Conferir os eventos e regras da Cloudflare para robôs verificados antes de alterar a proteção.

Os arquivos novos ainda precisam ser publicados. Não houve push, alteração de DNS, ajuste no painel da Cloudflare ou envio ao IndexNow nesta implementação. Após publicar, conferir o robots efetivamente entregue e limpar o cache necessário. O servidor de testes permanece sob controle do proprietário.

## Acessibilidade

As melhorias usam as WCAG 2.2 como referência, sem declarar conformidade integral. A home preserva textos nas imagens; isso limita a adaptação do texto da arte ao zoom, espaçamento e preferências de cor. Há alternativa em HTML para informações de atendimento, links de contato em texto e conteúdo descritivo para leitores de tela.

### Melhorias implementadas

- Atalhos de teclado com foco visível; na home, permitem chegar ao formulário ou à página de atendimento em texto. Os destinos internos recebem foco sem entrar na ordem normal de Tab.
- Conteúdo principal da home agrupado em `main`, incluindo imagens e formulário. O resumo visualmente oculto não contém mais links invisíveis que recebiam foco.
- Contexto textual nas imagens com mapas e nomes de ação nas áreas. Os mapas ficam ao lado das imagens correspondentes e há links equivalentes em texto no rodapé.
- Rótulo de campo obrigatório e instruções associadas por `aria-describedby`. O botão informa que abre o WhatsApp. A validação nativa de campo obrigatório foi mantida.
- Texto sobre o azul ajustado de razões de contraste de aproximadamente 3,80:1/4,04:1 para 5,02:1. Os links sobre branco têm 5,83:1 e os botões escuros com texto branco, 11:1. Esses cálculos cobrem as cores de HTML/CSS; não certificam os textos dentro das imagens.
- Áreas de toque de pelo menos 44 px de altura para controles principais, navegação e contatos em texto; os links de parágrafos mantêm o fluxo de leitura. As coordenadas da arte foram preservadas.
- Texto selecionável, campo de mensagem redimensionável, unidades relativas nas páginas internas e quebra de palavras longas.
- Regiões de tabelas acessíveis por teclado, identificadas pela legenda, com cabeçalhos e escopo de coluna.
- Aviso acessível de abertura em nova aba nos links que usam esse comportamento.
- Estilos para redução de movimento CSS, cores forçadas do sistema e impressão dos artigos.

### Validação e limites

Em 2026-11-23, o verificador local passou nas oito páginas. Na prévia já aberta pelo proprietário em `127.0.0.1:8080`, o Chrome expôs os nomes dos mapas, os rótulos e as instruções na árvore de acessibilidade. O primeiro Tab exibiu e focou o atalho para contato. O controle da janela ficou indisponível durante a continuação; isso não equivale a uma auditoria completa com leitor de tela.

Antes de publicar, completar a conferência manual:

1. Navegar com Tab, Shift+Tab e Enter, incluindo o salto para contato e para o conteúdo dos artigos. Conferir a visibilidade e a ordem do foco.
2. Testar o campo vazio e confirmar que a validação impede o encaminhamento. Para testar o fluxo com texto, conferir a mensagem aberta no WhatsApp sem enviá-la a menos que seja desejado.
3. Conferir larguras de 320 e 375 px, zoom de 200% e 400% e aumento de espaçamento de texto. Os artigos e controles devem continuar legíveis, sem sobreposição ou corte.
4. Usar VoiceOver ou NVDA para conferir títulos, landmarks, tabelas, instruções e links. Testar também alto contraste e redução de movimento no sistema.
5. Conferir as três artes após atualizações no Canva. Para remover a limitação de texto em imagem, será necessária uma futura composição equivalente em HTML, preservando a aparência desejada.

### Referências oficiais

- [Google: otimização para busca com IA](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google: recursos de IA e seu site](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: sitemaps e lastmod](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google: códigos HTTP](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)
- [Google: empresas com área de atendimento](https://support.google.com/business/answer/9157481)
- [OpenAI: robôs e permissões](https://developers.openai.com/api/docs/bots)
- [Proposta llms.txt](https://llmstxt.org/)
- [IndexNow: documentação](https://www.indexnow.org/documentation)
- [GitHub Pages: publicação estática e .nojekyll](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [W3C: WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/)
- [W3C: mapas de imagem acessíveis](https://www.w3.org/WAI/tutorials/images/imagemap/)
- [W3C: tamanho de alvos](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [W3C: instruções de formulário](https://www.w3.org/WAI/tutorials/forms/instructions/)
