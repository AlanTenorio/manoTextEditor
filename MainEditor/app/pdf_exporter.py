from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

def exportar_paginas_para_pdf(caminho_arquivo, lista_widgets_text):
    doc = SimpleDocTemplate(caminho_arquivo, pagesize=letter,
                            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    story = []
    styles = getSampleStyleSheet()
    align_map = {"left": TA_LEFT, "center": TA_CENTER, "right": TA_RIGHT}

    # Varre folha por folha do editor
    for pag_idx, widget_text in enumerate(lista_widgets_text):
        fim_linha = int(widget_text.index("end-1c").split(".")[0])

        for linha_idx in range(1, fim_linha + 1):
            alinhamento_linha = "left"
            tags_da_linha = widget_text.tag_names(f"{linha_idx}.0")
            for tag in ["left", "center", "right"]:
                if tag in tags_da_linha:
                    alinhamento_linha = tag
                    break

            estilo_paragrafo = ParagraphStyle(
                name=f"Estilo_P{pag_idx}_L{linha_idx}",
                parent=styles['Normal'],
                fontName="Helvetica",
                fontSize=11,
                leading=14,
                alignment=align_map[alinhamento_linha]
            )

            texto_linha_com_tags = ""
            conteudo_linha = widget_text.get(f"{linha_idx}.0", f"{linha_idx}.end")
            
            if not conteudo_linha:
                texto_linha_com_tags = "<br/>"
            else:
                for col_idx, caractere in enumerate(conteudo_linha):
                    indice_atual = f"{linha_idx}.{col_idx}"
                    tags_caractere = widget_text.tag_names(indice_atual)

                    char_formatado = caractere.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

                    if "bold" in tags_caractere:
                        char_formatado = f"<b>{char_formatado}</b>"
                    if "italic" in tags_caractere:
                        char_formatado = f"<i>{char_formatado}</i>"
                    if "underline" in tags_caractere:
                        char_formatado = f"<u>{char_formatado}</u>"

                    texto_linha_com_tags += char_formatado

            story.append(Paragraph(texto_linha_com_tags, estilo_paragrafo))
            story.append(Spacer(1, 2))

        # Se não for a última folha do documento, insere uma quebra de página explícita no PDF
        if pag_idx < len(lista_widgets_text) - 1:
            story.append(PageBreak())

    doc.build(story)