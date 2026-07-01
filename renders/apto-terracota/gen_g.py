# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Versão G — mais ousada, color-blocking orgânico com 3 cores (verde-oliva profundo,
terracota/ferrugem e creme). Pendente de palha, sem tapete. OpenRouter Flash com max_tokens capado."""
import base64, concurrent.futures, mimetypes, os, requests

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = "google/gemini-3.1-flash-image-preview"

CAMERA = ("TRAVA DE CÂMERA (absoluta): câmera FIXA, mesmo ângulo, altura, distância, zoom e enquadramento "
          "da original. NÃO gire/afaste/aproxime/endireite/reposicione a câmera.")
LAYOUT = ("LAYOUT e ARQUITETURA NÃO mudam: não mova/crie/remova/redimensione paredes, teto, piso, janelas "
          "ou portas. NÃO troque o PISO (porcelanato marmorizado bege/cinza-claro atual). Mantenha as mesmas "
          "luminárias de embutir do teto nos mesmos lugares.")
# Esquema mais OUSADO: color-blocking orgânico com 3 cores.
TECH_G = ("PINTURA OUSADA — COLOR-BLOCKING ORGÂNICO COM 3 CORES (evolução do estilo curvo das referências, "
          "porém mais colorido e marcante, ainda sofisticado e harmônico). Use exatamente TRÊS cores e "
          "distribua-as em zonas com bordas CURVAS orgânicas: "
          "(1) VERDE-OLIVA PROFUNDO (verde terroso escuro e encorpado) no TETO e na faixa SUPERIOR das paredes, "
          "escorrendo do teto para o alto; "
          "(2) TERRACOTA/FERRUGEM (laranja-queimado quente e saturado) em GRANDES BLOCOS ou ARCOS curvos que "
          "emolduram pontos focais do ambiente (por ex. atrás do sofá, ao redor do grande espelho, ou uma seção "
          "de parede inteira), com contornos arredondados orgânicos; "
          "(3) CREME/OFF-WHITE QUENTE (levemente amendoado) preenchendo o restante e a base das paredes, para dar "
          "respiro. Combine as 3 cores de forma EQUILIBRADA e intencional — mais ousada e saturada que as versões "
          "anteriores, com bom contraste, mas coordenada e elegante (não poluída). As transições entre cores são "
          "curvas suaves e bem-acabadas.")
MOOD = ("CLIMA: intimista, aconchegante e confortável, com personalidade. ILUMINAÇÃO INDIRETA e quente (fitas de "
        "LED discretas, luminárias, spots). MUITO IMPORTANTE: apesar da luz indireta, a imagem deve ficar BEM "
        "ILUMINADA e clara — NÃO escura nem subexposta. Fotorrealista, alta qualidade, estilo foto de revista.")
NO_RUG = "NÃO adicione NENHUM tapete ao ambiente — o piso de porcelanato fica totalmente à vista."
RACK = ("ADIÇÃO: instale um RACK/HACK de TV SOLTO (móvel independente apoiado no chão), NÃO embutido e NÃO "
        "fixado na parede, logo ABAIXO da TV pendurada — rack baixo horizontal de madeira clara/natural com pés "
        "aparentes. PROIBIDO: NÃO instale painel de madeira, painel ripado nem marcenaria atrás/embaixo da TV; a "
        "parede atrás da TV fica APENAS PINTADA, com a TV pendurada direto nela e só o rack solto no chão embaixo.")
PENDANT = ("ADIÇÃO: instale um PENDENTE (luminária de teto) centralizado SOBRE a MESA de jantar — cúpula de "
           "PALHA/RATTAN trançado em fibra natural, formato orgânico de sino/dome, luz quente, pendurado por um "
           "fio a partir do teto, na altura típica de pendente de jantar.")

P1 = ("VISTA: corredor de entrada olhando para a sala/jantar. Preserve EXATAMENTE, sem inventar nada novo: a "
      "mesa de jantar de tampo branco com pés de madeira e as cadeiras de madeira ao centro; a TV pendurada na "
      "parede ESQUERDA com a prateleira flutuante acima (aplique o rack solto embaixo dessa TV); ao fundo a "
      "cortina bege e o sofá verde-petróleo; à DIREITA o buffet/bancada de madeira, a estante preta vertical, o "
      "grande espelho de moldura preta, os pássaros de cerâmica, o prato verde e o prato vermelho com galinha.")
P2 = ("VISTA: centrada no GRANDE ESPELHO de chão com moldura preta. Preserve EXATAMENTE, sem inventar nada novo: "
      "o espelho ao centro (as paredes pintadas devem aparecer refletidas de forma coerente); a estante preta "
      "vertical à esquerda do espelho; o buffet/bancada de madeira à DIREITA com o mamão e o rack de metal preto "
      "com bananas; o macramé, o pequeno porta-retrato e a luminária de piso branca à esquerda; o prato verde e o "
      "prato vermelho com galinha na parede direita; a mesa de jantar e a cadeira em primeiro plano à esquerda.")
P3 = ("VISTA: parede do sofá (paisagem). Preserve EXATAMENTE o que JÁ aparece e NÃO acrescente NADA além do "
      "pendente pedido: a mesa de jantar de tampo branco com cadeiras de madeira à ESQUERDA; o sofá de veludo "
      "verde-petróleo de 2 lugares à DIREITA com as almofadas (redonda mostarda, branca texturizada e quadrada "
      "terracota) e o alto-falante preto no braço esquerdo; na parede do fundo os PÁSSAROS de cerâmica voando e o "
      "QUADRO da árvore; a CORTINA bege à direita do teto ao chão; a borda branca do balcão no canto inferior "
      "direito. PROIBIÇÃO ABSOLUTA (não existem nesta vista): NÃO adicione espelho, luminária de piso/abajur "
      "tripé, buffet/aparador, prateleiras, estante preta, parede de pratos, macramê, plantas, TV nem rack.")
P4 = ("VISTA: sala/jantar olhando para a cozinha ao fundo. Preserve EXATAMENTE, sem inventar nada novo: a TV "
      "pequena na parede ESQUERDA (aplique o rack solto embaixo dela); a estante preta vertical; o grande espelho "
      "com o macramê ao lado; a mesa de jantar de tampo branco com cadeiras de madeira; em primeiro plano o sofá "
      "verde-petróleo com a almofada redonda amarela e o alto-falante preto. Mantenha a cozinha ao fundo (geladeira, "
      "micro-ondas, armários de madeira, banquetas, plantas) e a porta branca inalteradas.")

PHOTOS = {
    "foto1": ("foto1.jpg", "9:16", P1, True, True),
    "foto2": ("foto2.jpg", "9:16", P2, False, False),
    "foto3": ("foto3.jpg", "16:9", P3, False, True),
    "foto4": ("foto4.jpg", "9:16", P4, True, True),
}


def data_url(path):
    with open(path, "rb") as f:
        d = f.read()
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(d).decode()}"


def build(view, has_tv, has_table):
    parts = ["INSTRUÇÃO DE EDIÇÃO — REDECORE este ambiente real a partir da fotografia.",
             CAMERA, LAYOUT, TECH_G, MOOD, NO_RUG]
    if has_tv:
        parts.append(RACK)
    if has_table:
        parts.append(PENDANT)
    parts.append(view)
    return " ".join(parts)


def gen(name, fname, aspect, view, has_tv, has_table, out):
    durl = data_url(os.path.join(BASE, fname))
    prompt = build(view, has_tv, has_table)
    last = ""
    for res, mt in [("2K", 6000), ("1K", 4000), ("1K", 3000)]:
        body = {"model": MODEL,
                "messages": [{"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": durl}},
                    {"type": "text", "text": prompt}]}],
                "modalities": ["image", "text"],
                "image_config": {"image_size": res, "aspect_ratio": aspect},
                "max_tokens": mt}
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                          json=body, timeout=300)
        if r.status_code == 200:
            try:
                url = r.json()["choices"][0]["message"]["images"][0]["image_url"]["url"]
            except Exception:
                last = f"sem imagem ({res})"; continue
            b64 = url.split(",", 1)[1] if "," in url else url
            with open(out, "wb") as f:
                f.write(base64.b64decode(b64))
            return name, True, res
        last = r.text[:150]
    return name, False, last


def main():
    outdir = os.path.join(BASE, "exploracao")
    os.makedirs(outdir, exist_ok=True)
    jobs = [(f"{pk}_G-3cores-ousada", f, a, v, tv, tb,
             os.path.join(outdir, f"{pk}_G-3cores-ousada.png"))
            for pk, (f, a, v, tv, tb) in PHOTOS.items()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for name, ok, msg in ex.map(lambda j: gen(*j), jobs):
            print(f"  [{'OK' if ok else 'FALHOU'}] {name}  :: {msg}")


if __name__ == "__main__":
    main()
