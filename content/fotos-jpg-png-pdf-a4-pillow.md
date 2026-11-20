Title: Como montar um PDF A4 com fotos JPG e PNG usando Pillow
Date: 2026-11-20 20:53
Slug: fotos-jpg-png-pdf-a4-pillow
Category: Python
Tags: python, pillow, pdf, imagens
Author: Zen
Github: zenoven
About_author: Colaborador do PDF Fan, com foco em ferramentas para trabalhar com documentos.

Uma turma prepara um material de leitura com uma capa em PNG e uma foto em JPG para imprimir. Na tela do celular, a foto parece estar em pé. No arquivo, porém, ela está deitada e depende de um campo EXIF para ser exibida na posição certa. A capa tem transparência. Se você simplesmente salvar essas imagens juntas em PDF, pode acabar com páginas de tamanhos diferentes ou com um fundo indesejado.

Vamos montar um PDF de duas páginas A4. O exemplo usa arquivos fictícios e roda localmente. A ordem vem de uma lista explícita de nomes, a orientação é normalizada e as imagens são encaixadas na página sem corte.

## Preparar o ambiente

Em um ambiente virtual com Python 3, instale o Pillow com `python -m pip install Pillow`. O código foi testado com Pillow 13.0.0. Este exemplo usa duas imagens estáticas, uma por página, e reserva uma margem de aproximadamente 10 mm. Para um material real, revise os direitos de uso das imagens antes de distribuí-lo.

## Definir a ordem, corrigir a orientação e encaixar

Em vez de depender da ordem dos arquivos na pasta, liste os caminhos na sequência em que o documento deve ser lido. O primeiro arquivo se torna a capa. Para facilitar o exemplo, todas as folhas são A4 em retrato a 150 dpi. Ajustamos a margem em pixels a partir de milímetros.

```python
from pathlib import Path

from PIL import Image, ImageOps


DPI = 150
PAGE = tuple(round(mm * DPI / 25.4) for mm in (210, 297))
MARGIN = round(10 * DPI / 25.4)
INNER = (PAGE[0] - 2 * MARGIN, PAGE[1] - 2 * MARGIN)
INPUTS = [Path("capa.png"), Path("foto.jpg")]


def make_page(path):
    with Image.open(path) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise ValueError(f"Use uma imagem estática: {path}")
        oriented = ImageOps.exif_transpose(source).convert("RGBA")
        oriented.thumbnail(INNER, Image.Resampling.LANCZOS)

        page = Image.new("RGB", PAGE, "white")
        position = ((PAGE[0] - oriented.width) // 2,
                    (PAGE[1] - oriented.height) // 2)
        page.paste(oriented, position, oriented.getchannel("A"))
        return page


pages = [make_page(path) for path in INPUTS]
pages[0].save("material-a4.pdf", save_all=True,
              append_images=pages[1:], dpi=(DPI, DPI))
```

`exif_transpose` aplica a orientação registrada na imagem antes de calcular o encaixe. O método `thumbnail` reduz imagens grandes sem alterar a proporção e sem ampliar as pequenas. Uma foto pequena vai ocupar menos espaço na folha, o que evita apresentar uma ampliação sem detalhe adicional como se tivesse qualidade para impressão.

Ao colar a imagem na folha, usamos o canal alfa como máscara. Assim, as áreas transparentes do PNG viram branco. `save_all` e `append_images` escrevem duas páginas no mesmo PDF. O PDF contém cópias rasterizadas das imagens, e o modo usado pelo Pillow pode recomprimir o conteúdo. O procedimento não cria texto pesquisável e não gera um PDF acessível por si só. Se o material tiver texto importante, ofereça uma versão em texto ou gere o PDF a partir de um documento que preserve o texto.

## Reproduzir com duas imagens fictícias

Para montar as entradas sem usar fotos reais, execute este pequeno script na mesma pasta do conversor. As cores e as dimensões são fáceis de reconhecer na saída. O marcador no canto do JPG ajuda a conferir se a rotação realmente aconteceu.

```python
from PIL import Image, ImageDraw

cover = Image.new("RGBA", (640, 360), (0, 0, 0, 0))
draw = ImageDraw.Draw(cover)
draw.rectangle((20, 20, 620, 340), fill=(22, 74, 143, 255))
draw.text((50, 55), "1 - CAPA", fill="white")
cover.save("capa.png")

photo = Image.new("RGB", (1200, 800), (245, 223, 175))
draw = ImageDraw.Draw(photo)
draw.rectangle((45, 45, 285, 180), fill=(170, 46, 39))
draw.text((66, 70), "2 - FOTO", fill="white")
exif = photo.getexif()
exif[274] = 6
photo.save("foto.jpg", exif=exif)
```

A tag EXIF 274 com valor 6 indica rotação de 90 graus no sentido horário para exibição. Ao rodar o conversor, a capa vem antes da foto, e a área original de 1200 por 800 pixels da segunda imagem passa a ter 800 por 1200 pixels antes do encaixe. Se você não usa Python e quer reproduzir a sequência manualmente com os mesmos arquivos fictícios, o [conversor de imagens para PDF do PDF Fan](https://pdf.fan/pt-br/imagem-para-pdf/) oferece seleção da ordem e formato A4. Colaboro com o PDF Fan. Confira a orientação na prévia de qualquer ferramenta que usar.

## Conferir antes de distribuir

1. Abra o PDF e confira o total de páginas e a ordem. Neste exemplo, são duas folhas e a capa vem primeiro.
2. Revise a orientação da foto, o fundo da capa e a legibilidade. Se precisar imprimir, veja também a prévia de impressão.
3. Com o Poppler instalado, `pdfinfo -f 1 -l 2 material-a4.pdf` mostra o tamanho das duas folhas. Os valores esperados são aproximadamente 595 por 842 pontos. A diferença de frações de ponto vem do arredondamento da quantidade de pixels.
4. Se o documento tiver muitas imagens, considere preparar lotes menores. O exemplo mantém as páginas em memória antes de gravar o PDF. Para fotos reais ou documentos restritos, use o fluxo local autorizado pela sua organização.

A referência de formatos do [Pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#pdf) explica as opções de gravação em PDF. A [documentação de ImageOps](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#PIL.ImageOps.exif_transpose) mostra como a orientação EXIF é aplicada.

*O texto teve assistência de IA. Os scripts e o arquivo PDF de exemplo foram verificados localmente com dados fictícios.*
