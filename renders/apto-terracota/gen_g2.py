# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Versão G2 (refinada, sóbria — nível CASA COR): teto pintado + meia-parede + parede inteira de
destaque, linhas RETAS, paleta muted (creme, terracota suave, verde-sálvia suave). Sem alucinações.
OpenRouter Flash com max_tokens capado."""
import base64, concurrent.futures, mimetypes, os, requests

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = "google/gemini-3.1-flash-image-preview"

CAMERA = ("TRAVA DE CÂMERA (absoluta): câmera FIXA, mesmo ângulo, altura, distância, zoom e enquadramento "
          "da original. NÃO gire/afaste/aproxime/endireite/reposicione a câmera.")
LAYOUT = ("LAYOUT e ARQUITETURA NÃO mudam: não mova/crie/remova/redimensione paredes, teto, piso, janelas "
          "ou portas. NÃO troque o PISO (porcelanato marmorizado bege/cinza-claro atual). Mantenha as mesmas "
          "luminárias de embutir do teto nos mesmos lugares.")
# Esquema SÓBRIO e elegante, com 3 técnicas clássicas de pintura e linhas RETAS.
TECH_G2 = ("PINTURA SÓBRIA E ELEGANTE, NÍVEL CASA COR (nada de circo). Combine, de forma discreta e "
           "sofisticada, TRÊS técnicas clássicas de pintura, SEMPRE com LINHAS RETAS, HORIZONTAIS E LIMPAS, "
           "acabamento impecável e composição equilibrada — PROIBIDO usar curvas orgânicas, ondas, arcos ou "
           "formas aleatórias. Use exatamente TRÊS cores MUTED e harmônicas: "
           "(A) CREME/BRANCO-CRU QUENTE; (B) TERRACOTA SUAVE/ARGILA (dessaturada, elegante); "
           "(C) VERDE-SÁLVIA SUAVE ACINZENTADO. Aplicação: "
           "1) TETO PINTADO num tom suave de CREME quente (levemente amendoado), uniforme; "
           "2) MEIA-PAREDE nas paredes: a BASE (até cerca de 1,1 m do piso) em TERRACOTA SUAVE e o TOPO em "
           "CREME, separados por uma LINHA RETA horizontal nivelada com um filete/frisо fino de arremate; "
           "3) UMA PAREDE INTEIRA de DESTAQUE (a parede focal do ambiente, do rodapé ao teto) pintada em "
           "VERDE-SÁLVIA SUAVE. Mantenha tudo sóbrio, atemporal e coordenado, como um projeto de interiores "
           "premiado — jamais poluído ou exagerado.")
MOOD = ("CLIMA: intimista, aconchegante, confortável e SOFISTICADO. ILUMINAÇÃO INDIRETA e quente (fitas de LED "
        "discretas, luminárias, spots). MUITO IMPORTANTE: apesar da luz indireta, a imagem deve ficar BEM "
        "ILUMINADA e clara — NÃO escura nem subexposta. Fotorrealista, alta qualidade, estilo revista de decoração.")
NO_RUG = "NÃO adicione NENHUM tapete — o piso de porcelanato fica totalmente à vista."
ANTI = ("ANTI-ALUCINAÇÃO (regra crítica): NÃO adicione NENHUM móvel, objeto, eletrodoméstico ou elemento que não "
        "exista na foto original. É EXPRESSAMENTE PROIBIDO acrescentar: banco, churrasqueira, poltrona, puff, mesa "
        "de centro/lateral, aparador extra, prateleiras novas, quadros novos, plantas novas ou luminárias além do "
        "pendente pedido. As ÚNICAS adições permitidas em toda a proposta são: (i) o rack de TV solto (apenas nas "
        "vistas em que a TV aparece) e (ii) o pendente de palha sobre a mesa de jantar. Todo o resto deve ser "
        "EXATAMENTE o que já existe na foto, nas mesmas posições.")
RACK = ("ADIÇÃO PERMITIDA: instale um RACK/HACK de TV SOLTO (móvel independente apoiado no chão), NÃO embutido e "
        "NÃO fixado na parede, logo ABAIXO da TV pendurada — rack baixo horizontal de madeira com pés aparentes. "
        "PROIBIDO painel/marcenaria atrás da TV; a parede atrás da TV fica só pintada, com a TV direto nela e "
        "apenas o rack solto embaixo.")
PENDANT = ("ADIÇÃO PERMITIDA: instale um PENDENTE de teto centralizado SOBRE a MESA de jantar — cúpula de "
           "PALHA/RATTAN trançado em fibra natural, formato de sino/dome, luz quente, pendurado por um fio.")

P1 = ("VISTA: corredor de entrada olhando para a sala/jantar. Preserve EXATAMENTE, sem inventar nada: a mesa de "
      "jantar de tampo branco com pés de madeira e as cadeiras de madeira ao centro; a TV na parede ESQUERDA com a "
      "prateleira flutuante acima (aplique o rack solto embaixo dessa TV); ao fundo a cortina bege e o sofá "
      "verde-petróleo; à DIREITA o buffet/bancada de madeira, a estante preta vertical, o grande espelho de moldura "
      "preta, os pássaros de cerâmica, o prato verde e o prato vermelho com galinha. Trate a parede de fundo (do "
      "sofá/cortina) como a PAREDE INTEIRA de destaque em verde-sálvia; as paredes laterais em meia-parede.")
P2 = ("VISTA: centrada no GRANDE ESPELHO de chão com moldura preta. Preserve EXATAMENTE, sem inventar nada: o "
      "espelho ao centro (as paredes pintadas aparecem refletidas de forma coerente); a estante preta vertical à "
      "esquerda do espelho; o buffet/bancada de madeira à DIREITA com o mamão e o rack de metal preto com bananas; o "
      "macramé, o porta-retrato e a luminária de piso branca à esquerda; o prato verde e o prato vermelho com "
      "galinha na parede direita; a mesa de jantar e a cadeira em primeiro plano à esquerda. A parede do espelho "
      "pode ser a PAREDE INTEIRA de destaque em verde-sálvia; as demais em meia-parede.")
P3 = ("VISTA: parede do sofá (paisagem). Preserve EXATAMENTE o que JÁ aparece e NÃO acrescente NADA além do "
      "pendente: a mesa de jantar de tampo branco com cadeiras de madeira à ESQUERDA; o sofá de veludo "
      "verde-petróleo de 2 lugares à DIREITA com as almofadas (redonda mostarda, branca texturizada e quadrada "
      "terracota) e o alto-falante preto no braço esquerdo; na parede do fundo os PÁSSAROS de cerâmica voando e o "
      "QUADRO da árvore; a CORTINA bege à direita do teto ao chão; a borda branca do balcão no canto inferior "
      "direito. A parede do fundo (com os pássaros e o quadro) é a PAREDE INTEIRA de destaque em verde-sálvia. "
      "PROIBIÇÃO: NÃO adicione espelho, abajur tripé, buffet, prateleiras, estante, pratos, macramê, plantas, TV "
      "nem rack nesta vista.")
P4 = ("VISTA: sala/jantar olhando para a cozinha ao fundo. Preserve EXATAMENTE, sem inventar nada: a TV pequena na "
      "parede ESQUERDA (aplique o rack solto embaixo dela); a estante preta vertical; o grande espelho com o macramê "
      "ao lado; a mesa de jantar de tampo branco com cadeiras de madeira; em primeiro plano o sofá verde-petróleo "
      "com a almofada redonda amarela e o alto-falante preto. Mantenha a cozinha ao fundo (geladeira, micro-ondas, "
      "armários de madeira, banquetas, plantas) e a porta branca inalteradas. As paredes laterais em meia-parede; a "
      "parede do espelho pode ser a de destaque em verde-sálvia.")

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
             CAMERA, LAYOUT, TECH_G2, MOOD, NO_RUG, ANTI]
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
    jobs = [(f"{pk}_G2-casacor", f, a, v, tv, tb,
             os.path.join(outdir, f"{pk}_G2-casacor.png"))
            for pk, (f, a, v, tv, tb) in PHOTOS.items()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for name, ok, msg in ex.map(lambda j: gen(*j), jobs):
            print(f"  [{'OK' if ok else 'FALHOU'}] {name}  :: {msg}")


if __name__ == "__main__":
    main()
