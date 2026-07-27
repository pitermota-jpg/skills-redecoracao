# Skills de Redecoração para Claude

Três skills que trabalham juntas para redecorar ambientes a partir de uma foto:

- **redecoracao** — gera mockups de redecoração a partir da foto de um cômodo (vários estilos de uma vez).
- **nano-banana-pro** — motor de geração/edição de imagens (Google Nano Banana Pro / Gemini). Usado pelas outras duas.
- **busca-produtos** — busca por imagem (Google Lens via SerpAPI) para descobrir **onde comprar** os itens da cena.

Além delas, o repositório inclui a skill oficial do [notebooklm-py](https://github.com/teng-lin/notebooklm-py):

- **notebooklm** — acesso programático ao Google NotebookLM (criar notebooks, adicionar fontes, gerar
  podcasts/vídeos/quizzes/flashcards, etc.). Instalada a partir do próprio pacote com
  `notebooklm skill install`. Veja a seção [NotebookLM](#notebooklm) abaixo.

## Como instalar

### Opção 1 — peça ao Claude (mais fácil)

Clone o repositório e peça ao Claude para instalar:

```bash
git clone https://github.com/rtadewald/skills-redecoracao.git
```

Depois, no Claude Code, é só pedir:

> "Instale as skills que estão em `~/skills-redecoracao` no meu Claude."

O Claude copia as três pastas para `~/.claude/skills/` para você.

### Opção 2 — manual

Copie as três pastas para o diretório de skills do Claude:

```bash
git clone https://github.com/rtadewald/skills-redecoracao.git
cp -r skills-redecoracao/nano-banana-pro ~/.claude/skills/
cp -r skills-redecoracao/busca-produtos  ~/.claude/skills/
cp -r skills-redecoracao/redecoracao     ~/.claude/skills/
```

Mantenha os nomes das pastas — as skills se referenciam por caminho.

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) instalado (os scripts rodam com `uv run`).
- Chaves de API no `.env` (ou variáveis de ambiente). **Nenhuma chave vem no repositório.**

| Variável | Para quê | Obrigatória? |
|---|---|---|
| `OPENROUTER_API_KEY` | geração de imagem (padrão) | uma das duas |
| `GEMINI_API_KEY` | geração de imagem (alternativa) | uma das duas |
| `SERPAPI_API_KEY` | busca de produtos (onde comprar) | só para `busca-produtos` |
| `IMGBB_API_KEY` | upload de imagem na busca (opcional) | não |

## Como usar

No Claude, basta pedir em linguagem natural, por exemplo:

> "Redecora esse quarto como um estúdio de gravação." (anexe a foto)

O Claude aciona a skill **redecoracao**, gera os mockups e, se você quiser, usa a **busca-produtos** para achar onde comprar cada item.

## NotebookLM

A skill **notebooklm** dá acesso ao [Google NotebookLM](https://notebooklm.google.com/) pela linha
de comando. Ela é a skill oficial mantida junto com o pacote [notebooklm-py](https://github.com/teng-lin/notebooklm-py)
e vive em `.claude/skills/notebooklm/`.

### Instalar / atualizar

```bash
# CLI (traz o navegador Playwright para o login)
uv tool install "notebooklm-py[browser]"

# (re)instala a skill neste projeto — sobrescreve com --force ao atualizar
notebooklm skill install --scope project --target claude
```

### Autenticar (uma vez, precisa de navegador)

```bash
notebooklm login      # abre o navegador para login no Google
notebooklm doctor     # confere auth e configuração do perfil
```

> O `login` é interativo e depende de navegador — rode na **sua máquina**, não num ambiente remoto/headless.

### Uso rápido

```bash
notebooklm create "Minhas notas" --use
notebooklm source add "https://exemplo.com/artigo"     # URL, arquivo, YouTube ou texto
notebooklm ask "quais são os temas principais?"
notebooklm generate audio "deep dive sobre os pontos-chave" --wait
notebooklm download audio ./podcast.mp3
```

No Claude Code, basta pedir em linguagem natural (ex.: *"crie um podcast sobre esses PDFs"*) ou
chamar `/notebooklm` — a skill traduz o pedido nos comandos acima.
