# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Versão F em LINHA RETA (linha na altura do batente da porta) para as paredes gerais,
com a parede da TV e a parede do quarto ao fundo em Versão C + rack mid-century.
5 visões. OpenRouter Flash com max_tokens capado."""
import base64, concurrent.futures, mimetypes, os, requests

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = "google/gemini-3.1-flash-image-preview"

CAMERA = ("TRAVA DE CÂMERA (absoluta): câmera FIXA, mesmo ângulo, altura, distância, zoom e enquadramento "
          "da original. NÃO gire/afaste/aproxime/endireite/reposicione a câmera.")
LAYOUT = ("LAYOUT e ARQUITETURA NÃO mudam: não mova/crie/remova/redimensione paredes, teto, piso, janelas "
          "ou portas. NÃO troque o PISO (porcelanato marmorizado bege/cinza-claro atual). Mantenha as mesmas "
          "luminárias de embutir do teto nos mesmos lugares.")
PAINT_F = ("PINTURA GERAL — VERSÃO F EM LINHA RETA (SEM CURVAS): pinte o TETO e a FAIXA SUPERIOR das paredes "
           "gerais em TERRACOTA/ARGILA SUAVE (muted, dessaturada, quente), descendo do teto até uma LINHA "
           "HORIZONTAL RETA, nivelada e contínua, na ALTURA DO TOPO DO BATENTE/VERGA DA PORTA (a mesma altura do "
           "topo do marco da porta do quarto que aparece à direita, ~2,10 m do piso). Da linha para baixo, a "
           "parede fica em CREME/OFF-WHITE QUENTE. A divisão é uma linha RETA e limpa — É PROIBIDO usar curvas, "
           "ondas, arcos ou cantos arredondados em qualquer parede.")
PAINT_C = ("EXCEÇÃO — VERSÃO C (nas paredes indicadas na descrição da vista): NÃO use o efeito F nessas paredes. "
           "Pinte a parte SUPERIOR (os 2/3 de cima) em CREME/OFF-WHITE claro e apenas o TERÇO INFERIOR (1/3 de "
           "baixo) em TERRACOTA suave, com uma linha divisória horizontal RETA a ~1/3 da altura a partir do "
           "rodapé. O trecho de TETO logo acima dessas paredes permanece CLARO (off-white).")
RACK = ("RACK/HACK DE TV (na parede da TV): sob a TV pendurada, coloque um RACK SOLTO de madeira (nogueira), "
        "mid-century, com DUAS PORTAS PRETAS laterais (preto fosco), nicho central aberto com prateleira, tampo de "
        "madeira e PÉS-PALITO de madeira inclinados. Móvel independente apoiado no chão (não embutido, não fixado "
        "na parede). PROIBIDO painel/marcenaria atrás da TV: a TV fica pendurada direto na parede pintada. As "
        "portas ajudam a esconder os cabos — organize/oculte os cabos soltos, deixando o visual limpo.")
PENDANT = ("PENDENTE (só onde houver mesa de jantar visível): instale um pendente de teto centralizado SOBRE a "
           "MESA de jantar — cúpula de PALHA/RATTAN trançado, formato de sino/dome, luz quente, por um fio.")
MOOD = ("CLIMA: intimista, aconchegante e confortável. ILUMINAÇÃO INDIRETA e quente. MUITO IMPORTANTE: a imagem "
        "deve ficar BEM ILUMINADA e clara — NÃO escura nem subexposta. Fotorrealista, estilo revista de decoração.")
NO_RUG = "NÃO adicione NENHUM tapete — o piso fica à vista."
ANTI = ("ANTI-ALUCINAÇÃO (crítico): NÃO adicione móveis, objetos, eletrodomésticos ou elementos que não existam na "
        "foto original. PROIBIDO: banco, churrasqueira, poltrona, puff, mesa lateral/central, aparadores extras, "
        "prateleiras novas, quadros novos, plantas novas, luminárias além do pendente. As ÚNICAS adições permitidas "
        "são: (i) o rack de TV mid-century sob a TV (na parede da TV) e (ii) o pendente de palha sobre a mesa. Todo "
        "o resto é EXATAMENTE o que já existe na foto, nas mesmas posições.")

P1 = ("VISTA: corredor de entrada olhando para a sala/jantar. PAREDE DA TV = VERSÃO C + RACK: é a parede ESQUERDA, "
      "onde está a TV com a PRATELEIRA FLUTUANTE branca acima — pinte-a em Versão C e coloque o rack mid-century "
      "sob a TV. Se aparecer a porta do quarto ao fundo, a parede dela também é Versão C. TODAS as demais paredes e "
      "o teto = VERSÃO F EM LINHA RETA. Preserve: a mesa de jantar de tampo branco com cadeiras de madeira ao "
      "centro; ao fundo a cortina e o sofá verde-petróleo; à DIREITA o buffet/bancada de madeira, a estante preta, "
      "o grande espelho de moldura preta, os pássaros de cerâmica, o prato verde e o prato vermelho. Pendente de "
      "palha sobre a mesa.")
P2 = ("VISTA: centrada no GRANDE ESPELHO de chão com moldura preta. PAREDE DA TV = VERSÃO C + RACK: à ESQUERDA, "
      "onde aparecem a TV e a prateleira — Versão C e rack sob a TV. Se a porta do quarto aparecer ao fundo, sua "
      "parede é Versão C. A parede do ESPELHO e as demais = VERSÃO F EM LINHA RETA. Preserve: o espelho ao centro "
      "(refletindo as paredes de forma coerente); a estante preta à esquerda do espelho; o buffet de madeira à "
      "DIREITA com o mamão e o rack de metal preto com bananas; o macramé, o porta-retrato e a luminária de piso "
      "branca à esquerda; o prato verde e o prato vermelho; a mesa e a cadeira em primeiro plano à esquerda.")
P3 = ("VISTA: parede do sofá (paisagem). NÃO há parede de TV nesta vista: aplique VERSÃO F EM LINHA RETA em TODAS "
      "as paredes e no teto (linha reta na altura do batente ~2,10 m). Preserve EXATAMENTE, sem inventar nada além "
      "do pendente: a mesa de jantar de tampo branco com cadeiras de madeira à ESQUERDA; o sofá de veludo "
      "verde-petróleo à DIREITA com as almofadas (redonda mostarda, branca texturizada e quadrada terracota) e o "
      "alto-falante preto; na parede do fundo os PÁSSAROS de cerâmica e o QUADRO da árvore; a CORTINA bege à "
      "direita; a borda branca do balcão no canto inferior direito. Pendente de palha sobre a mesa. NÃO adicione "
      "espelho, estante, buffet, prateleiras, plantas, TV nem rack.")
P4 = ("VISTA: sala/jantar olhando para a cozinha ao fundo. PAREDE DA TV = VERSÃO C + RACK: é a parede ESQUERDA, "
      "com a TV pequena — Versão C e rack mid-century sob a TV. A parede do fundo com a PORTA branca (parede do "
      "quarto/entrada ao fundo) = VERSÃO C. As demais paredes e o teto = VERSÃO F EM LINHA RETA. Preserve: a "
      "estante preta; o grande espelho com o macramê ao lado; a mesa de jantar de tampo branco com cadeiras; em "
      "primeiro plano o sofá verde-petróleo com a almofada redonda amarela; a cozinha ao fundo (geladeira, "
      "micro-ondas, armários de madeira, banquetas, plantas). Pendente de palha sobre a mesa.")
PTV = ("VISTA: canto da TV (close). TODA a parede visível da TV = VERSÃO C (2/3 de cima em creme, 1/3 de baixo em "
       "terracota, teto claro) + o RACK mid-century (madeira, duas portas pretas, nicho central, pés-palito) sob a "
       "TV. A passagem/porta à DIREITA (parede do quarto ao fundo) = VERSÃO C. NÃO aplique F nesta vista. Preserve "
       "EXATAMENTE: a TV pendurada; a PRATELEIRA FLUTUANTE branca acima com TODOS os objetos (pera de madeira com "
       "folhas, galo amarelo, figuras de madeira, caveira colorida, casinhas, castiçais e velas); a CORTINA taupe "
       "à ESQUERDA (porta de vidro, esquadria preta); a LUMINÁRIA DE PISO preta; o corredor à direita; o rodapé. "
       "NÃO há mesa aqui, portanto NÃO adicione pendente.")

# (arquivo, aspecto, view, tem_tv, tem_mesa)
PHOTOS = {
    "foto1":   ("foto1.jpg",  "9:16", P1,  True,  True),
    "foto2":   ("foto2.jpg",  "9:16", P2,  True,  False),
    "foto3":   ("foto3.jpg",  "16:9", P3,  False, True),
    "foto4":   ("foto4.jpg",  "9:16", P4,  True,  True),
    "foto_tv": ("foto_tv.jpg","9:16", PTV, True,  False),
}


def data_url(path):
    with open(path, "rb") as f:
        d = f.read()
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(d).decode()}"


def build(view, has_tv, has_table):
    parts = ["INSTRUÇÃO DE EDIÇÃO — REDECORE este ambiente real a partir da fotografia.",
             CAMERA, LAYOUT, PAINT_F, PAINT_C]
    if has_tv:
        parts.append(RACK)
    if has_table:
        parts.append(PENDANT)
    parts += [MOOD, NO_RUG, ANTI, view]
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
    jobs = [(f"{pk}_Freta", f, a, v, tv, tb, os.path.join(outdir, f"{pk}_Freta.png"))
            for pk, (f, a, v, tv, tb) in PHOTOS.items()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for name, ok, msg in ex.map(lambda j: gen(*j), jobs):
            print(f"  [{'OK' if ok else 'FALHOU'}] {name}  :: {msg}")


if __name__ == "__main__":
    main()
