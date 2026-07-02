# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Corrige foto1, foto2, foto4: Versão F em LINHA RETA pura (terracota do teto até a linha na
altura do batente; ABAIXO tudo creme liso, SEM faixa/dado de terracota embaixo). Mantém rack e
pendente. OpenRouter Flash com max_tokens capado."""
import base64, concurrent.futures, mimetypes, os, requests

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = "google/gemini-3.1-flash-image-preview"

CAMERA = ("TRAVA DE CÂMERA (absoluta): câmera FIXA, mesmo ângulo, altura, distância, zoom e enquadramento "
          "da original. NÃO gire/afaste/aproxime/endireite/reposicione a câmera.")
LAYOUT = ("LAYOUT e ARQUITETURA NÃO mudam: não mova/crie/remova/redimensione paredes, teto, piso, janelas "
          "ou portas. NÃO troque o PISO (porcelanato marmorizado bege/cinza-claro atual). Mantenha as mesmas "
          "luminárias de embutir do teto nos mesmos lugares.")
PAINT = ("PINTURA — VERSÃO F EM LINHA RETA (SEM CURVAS): pinte o TETO e a FAIXA SUPERIOR de TODAS as paredes em "
         "TERRACOTA/ARGILA SUAVE (muted, quente), descendo do teto até UMA ÚNICA LINHA HORIZONTAL RETA e nivelada "
         "na ALTURA DO TOPO DO BATENTE DA PORTA (~2,10 m do piso). ABAIXO dessa linha, TODA a parede é "
         "CREME/OFF-WHITE QUENTE, lisa e uniforme, até o rodapé. "
         "REGRA CRÍTICA: NÃO pinte NENHUMA faixa, barra, dado ou meia-parede de terracota na PARTE DE BAIXO das "
         "paredes nem junto ao rodapé — a metade inferior é 100% CREME liso, sem segunda cor. Existe APENAS UMA "
         "divisão de cor: a linha reta no alto (na altura do batente). PROIBIDO curvas, ondas, arcos e qualquer "
         "faixa terrosa inferior.")
RACK = ("RACK/HACK DE TV: sob a TV pendurada, coloque um RACK SOLTO de madeira (nogueira), mid-century, com DUAS "
        "PORTAS PRETAS laterais, nicho central aberto e PÉS-PALITO inclinados. Móvel independente apoiado no chão "
        "(não embutido, não fixado na parede). PROIBIDO painel/marcenaria atrás da TV; a TV fica direto na parede "
        "pintada. As portas ajudam a esconder os cabos — deixe o visual limpo.")
PENDANT = ("PENDENTE sobre a MESA de jantar: cúpula de PALHA/RATTAN trançado, formato de sino/dome, luz quente, "
           "pendurado por um fio, centralizado sobre a mesa.")
MOOD = ("CLIMA: intimista, aconchegante, confortável. ILUMINAÇÃO INDIRETA e quente. MUITO IMPORTANTE: a imagem "
        "deve ficar BEM ILUMINADA e clara — NÃO escura nem subexposta. Fotorrealista, estilo revista de decoração.")
NO_RUG = "NÃO adicione NENHUM tapete — o piso fica à vista."
ANTI = ("ANTI-ALUCINAÇÃO (crítico): NÃO adicione móveis, objetos ou elementos que não existam na foto original "
        "(nada de banco, churrasqueira, poltrona, mesa lateral, aparadores/prateleiras/quadros/plantas novos, nem "
        "luminárias além do pendente). ÚNICAS adições: o rack mid-century sob a TV e o pendente de palha sobre a "
        "mesa. Todo o resto é EXATAMENTE o que já existe, nas mesmas posições.")

P1 = ("VISTA: corredor de entrada olhando para a sala/jantar. Aplique a pintura F EM LINHA RETA em TODAS as "
      "paredes e no teto (uma única linha reta no alto, na altura do batente; abaixo tudo creme liso, SEM faixa "
      "terrosa embaixo). A TV está na parede ESQUERDA (com a prateleira flutuante branca acima) — coloque o rack "
      "mid-century sob ela. Preserve: a mesa de jantar de tampo branco com cadeiras de madeira ao centro; ao fundo "
      "a cortina e o sofá verde-petróleo; à DIREITA o buffet/bancada de madeira, a estante preta, o grande espelho "
      "de moldura preta, os pássaros de cerâmica, o prato verde e o prato vermelho. Pendente de palha sobre a mesa.")
P2 = ("VISTA: centrada no GRANDE ESPELHO de chão com moldura preta. Aplique a pintura F EM LINHA RETA em TODAS as "
      "paredes e no teto (uma única linha reta no alto; abaixo tudo creme liso, SEM faixa terrosa embaixo). A TV "
      "aparece à ESQUERDA — coloque o rack mid-century sob ela. Preserve: o espelho ao centro (refletindo as "
      "paredes de forma coerente); a estante preta à esquerda do espelho; o buffet de madeira à DIREITA com o "
      "mamão e o rack de metal preto com bananas; o macramé, o porta-retrato e a luminária de piso branca à "
      "esquerda; o prato verde e o prato vermelho; a mesa e a cadeira em primeiro plano à esquerda.")
P4 = ("VISTA: sala/jantar olhando para a cozinha ao fundo. Aplique a pintura F EM LINHA RETA em TODAS as paredes e "
      "no teto (uma única linha reta no alto, na altura do batente da porta branca do fundo; abaixo tudo creme "
      "liso, SEM faixa terrosa embaixo). A TV pequena está na parede ESQUERDA — coloque o rack mid-century sob "
      "ela. Preserve: a estante preta; o grande espelho com o macramê ao lado; a mesa de jantar de tampo branco "
      "com cadeiras; em primeiro plano o sofá verde-petróleo com a almofada redonda amarela; a cozinha ao fundo "
      "(geladeira, micro-ondas, armários de madeira, banquetas, plantas) e a porta branca. Pendente de palha "
      "sobre a mesa.")

PHOTOS = {
    "foto1": ("foto1.jpg", "9:16", P1, True,  True),
    "foto2": ("foto2.jpg", "9:16", P2, True,  False),
    "foto4": ("foto4.jpg", "9:16", P4, True,  True),
}


def data_url(path):
    with open(path, "rb") as f:
        d = f.read()
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(d).decode()}"


def build(view, has_tv, has_table):
    parts = ["INSTRUÇÃO DE EDIÇÃO — REDECORE este ambiente real a partir da fotografia.",
             CAMERA, LAYOUT, PAINT]
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
    jobs = [(f"{pk}_Freta2", f, a, v, tv, tb, os.path.join(outdir, f"{pk}_Freta2.png"))
            for pk, (f, a, v, tv, tb) in PHOTOS.items()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for name, ok, msg in ex.map(lambda j: gen(*j), jobs):
            print(f"  [{'OK' if ok else 'FALHOU'}] {name}  :: {msg}")


if __name__ == "__main__":
    main()
