# /// script
# requires-python = ">=3.10"
# ///
"""Orquestrador custom: 4 visões x 2 variantes de cor terracota, em paralelo."""
import concurrent.futures, os, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
NANO = "/home/user/skills-redecoracao/.claude/skills/nano-banana-pro/scripts/generate_image.py"
PROVIDER = "openrouter"
MODEL = "google/gemini-3-pro-image-preview"  # Pro: melhor fidelidade/preservação
RES = "2K"

# ---------- BLOCOS COMUNS ----------
CAMERA = (
    "TRAVA DE CÂMERA (regra absoluta): a câmera é FIXA. Mantenha EXATAMENTE o mesmo ângulo, "
    "altura, distância, lente, zoom e enquadramento da foto original — a MESMA porção do cômodo "
    "visível e a MESMA perspectiva de paredes, teto e piso. NÃO gire, NÃO afaste, NÃO aproxime, "
    "NÃO endireite, NÃO reposicione a câmera. A nova foto é tirada do mesmíssimo tripé."
)
LAYOUT = (
    "REGRA INVIOLÁVEL — o LAYOUT e a ARQUITETURA NÃO mudam: não mova, crie, remova ou redimensione "
    "paredes, divisórias, colunas, teto ou piso; não mexa em janelas e portas (cada abertura fica no "
    "MESMO lugar, tamanho e formato). NÃO troque o PISO: mantenha exatamente o porcelanato marmorizado "
    "bege/cinza-claro atual, com o mesmo desenho e veios. O teto permanece claro (off-white) e plano, "
    "com as mesmas luminárias de embutir nos mesmos lugares."
)
PRESERVE = (
    "PRESERVE AO MÁXIMO os itens atuais, exatamente onde estão e com as mesmas cores, formas e "
    "materiais: a mesa de jantar de tampo branco com pés de madeira e as cadeiras de madeira com "
    "assento estofado claro; o sofá de veludo verde-petróleo com as almofadas (amarela redonda, "
    "branca texturizada e laranja/terracota); o grande espelho de chão com moldura preta fina; a "
    "estante/prateleira preta vertical de metal; o balcão/buffet de madeira (bancada) à direita; os "
    "pássaros de cerâmica voando na parede; o quadro da árvore; os pratos decorativos (um verde e um "
    "vermelho com galinha); o macramê; a luminária de piso; os vasos e plantas (espada-de-são-jorge). "
    "Não invente móveis novos além do que for explicitamente pedido."
)
RACK = (
    "ADIÇÃO PEDIDA: instale um RACK/HACK de TV SOLTO (móvel independente apoiado no chão), NÃO embutido "
    "e NÃO fixado na parede, logo ABAIXO da TV que está pendurada na parede. É um rack baixo e horizontal, "
    "de madeira (com detalhes em preto), pés aparentes, linha leve e clean, combinando com o buffet de "
    "madeira existente. A TV continua pendurada na parede; o rack apenas repousa no piso embaixo dela. "
    "Não transforme em painel ripado embutido — ele deve parecer um móvel solto."
)
MOOD = (
    "CLIMA: ambiente intimista, aconchegante e confortável. ILUMINAÇÃO INDIRETA e quente (fitas de LED "
    "em sancas/atrás de móveis, luminárias de piso e de mesa, spots suaves), criando camadas de luz "
    "acolhedoras. MUITO IMPORTANTE: apesar da luz indireta, a imagem deve ficar BEM ILUMINADA e clara o "
    "suficiente para ver todos os detalhes — NÃO deixe a foto escura, subexposta ou sombria. Resultado "
    "fotorrealista, alta qualidade, como foto de revista de decoração."
)

# ---------- VARIANTES DE COR ----------
COLOR_A = (
    "PINTURA (color-drench): pinte TODAS as paredes do ambiente numa única cor terrosa, quente e "
    "envolvente — terracota/chocolate, porém um pouco MAIS CLARA e mais avermelhada/terracota (tom de "
    "argila quente, terracota queimada), NÃO marrom escuro pesado. Todas as paredes na MESMA cor, do "
    "rodapé ao teto (color-drench). O TETO permanece CLARO (off-white). A iluminação indireta é quente "
    "e realça o tom terroso das paredes."
)
COLOR_B = (
    "PINTURA (color-drench terroso com arremate claro): pinte TODAS as paredes na MESMA cor terrosa "
    "quente — terracota/chocolate um pouco mais clara e avermelhada (tom de argila quente). PORÉM deixe "
    "uma FAIXA HORIZONTAL CLARA contínua de cerca de 20 cm de altura no TOPO de todas as paredes, "
    "encostada no teto, pintada na MESMA cor clara (off-white) do teto — como se o teto descesse um "
    "pouco pela parede (efeito de arremate/sanca pintada). Ou seja: teto claro + faixa clara de ~20cm no "
    "alto da parede + restante da parede em terracota. A faixa deve ser uniforme e contornar o ambiente. "
    "O TETO permanece claro. Iluminação indireta quente, imagem bem iluminada."
)

# ---------- ESPECÍFICOS POR FOTO ----------
P1 = ("VISTA: corredor de entrada olhando para a sala/jantar integrada. A TV está pendurada na parede "
      "ESQUERDA (com uma prateleira flutuante acima); aplique o rack solto embaixo dessa TV. Ao fundo, "
      "a cortina e o sofá; à direita, o buffet de madeira e a estante preta com o espelho.")
P2 = ("VISTA: ambiente centrado no GRANDE ESPELHO de chão com moldura preta, com a estante preta à "
      "esquerda dele e o buffet de madeira à direita; mesa de jantar à esquerda. As paredes terrosas "
      "devem aparecer também REFLETIDAS no espelho, de forma coerente. Se houver TV refletida/visível, "
      "mantenha. Preserve os pratos decorativos e o macramê.")
P3 = ("VISTA: parede do sofá. Sofá de veludo verde-petróleo, o quadro da árvore e os pássaros de "
      "cerâmica voando na parede, a mesa de jantar branca à esquerda e a cortina à direita. NÃO há TV "
      "visível nesta vista, portanto NÃO adicione rack aqui. Recupere/uniformize qualquer mancha da "
      "parede ao pintá-la. Mantenha os pássaros e o quadro.")
P4 = ("VISTA: sala/jantar olhando para a cozinha ao fundo. A TV pequena está na parede ESQUERDA; "
      "aplique o rack solto embaixo dela. Há o espelho grande com macramê, a estante preta, a mesa de "
      "jantar e, em primeiro plano, o sofá verde com a almofada amarela. Mantenha a cozinha, a geladeira "
      "e a porta ao fundo inalteradas.")

PHOTOS = {
    "foto1": ("foto1.jpg", "9:16", P1, True),
    "foto2": ("foto2.jpg", "9:16", P2, False),
    "foto3": ("foto3.jpg", "16:9", P3, False),
    "foto4": ("foto4.jpg", "9:16", P4, True),
}
VARIANTS = {"A-colordrench": COLOR_A, "B-faixa": COLOR_B}


def build_prompt(view_txt, color_txt, has_tv):
    parts = [
        "INSTRUÇÃO DE EDIÇÃO — REDECORE este ambiente real a partir da fotografia, respeitando os limites abaixo.",
        CAMERA, LAYOUT, PRESERVE,
    ]
    if has_tv:
        parts.append(RACK)
    parts += [MOOD, color_txt, view_txt]
    return " ".join(parts)


def gen(name, fname, aspect, view_txt, color_txt, has_tv, out):
    prompt = build_prompt(view_txt, color_txt, has_tv)
    cmd = ["uv", "run", NANO, "--prompt", prompt, "--filename", out,
           "--resolution", RES, "--aspect-ratio", aspect,
           "--input-image", os.path.join(BASE, fname),
           "--provider", PROVIDER, "--model", MODEL]
    p = subprocess.run(cmd, capture_output=True, text=True)
    ok = p.returncode == 0 and os.path.isfile(out)
    return name, ok, (p.stderr or p.stdout).strip()[-300:]


def main():
    outdir = os.path.join(BASE, "exploracao")
    os.makedirs(outdir, exist_ok=True)
    jobs = []
    for pk, (fname, aspect, view, has_tv) in PHOTOS.items():
        for vk, color in VARIANTS.items():
            out = os.path.join(outdir, f"{pk}_{vk}.png")
            jobs.append((f"{pk}_{vk}", fname, aspect, view, color, has_tv, out))
    print(f"Gerando {len(jobs)} imagens (Pro {RES})...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(gen, *j) for j in jobs]
        for f in concurrent.futures.as_completed(futs):
            name, ok, msg = f.result()
            print(f"  [{'OK' if ok else 'FALHOU'}] {name}" + ("" if ok else f"  :: {msg}"))


if __name__ == "__main__":
    main()
