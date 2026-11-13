from os import environ
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "grokking-deep-learning-chapter-1.pdf"
MANNING = "https://manning-content.s3.amazonaws.com/download/d/5d0f2b3-4591-4648-a869-6dafc6f38310/sample_ch01_Trask2_Grokking_Deep-Learning_corr_January06.pdf"
PITER = "https://www.piter.com/collection/programmirovanie-osnovy-i-algoritmy/product/grokaem-glubokoe-obuchenie"

PAPER = HexColor("#F8F5EC")
INK = HexColor("#202C28")
ACCENT = HexColor("#345644")
MUTED = HexColor("#535F55")
RULE = HexColor("#CFCFC0")
TINT = HexColor("#E5EBDF")

FONTS = Path(environ.get("POLYA_PDF_FONTS", "C:/Windows/Fonts"))
for name, filename in (
    ("Georgia", "georgia.ttf"),
    ("GeorgiaItalic", "georgiai.ttf"),
    ("Segoe", "segoeui.ttf"),
    ("SegoeSemibold", "seguisb.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))

COPY = {
    "idea": "Траск предлагает освоить глубокое обучение, собирая нейросети с нуля. Так можно увидеть, как модели автоматизируют отдельные интеллектуальные задачи.",
    "applications": "Нейросети применяют для анализа изображений, распознавания речи и перевода. Сходные принципы работают в разных областях.",
    "automation": "В 2019 году Траск предполагал, что автоматизация затронет операторов колл-центров, водителей и младших аналитиков.",
    "creative": "Автор предлагает представить модель, которая учится рисовать в стиле Моне на примерах картин.",
    "framework": "Траск сравнивает освоение фреймворка с изучением гоночной машины. Водителю нужны и навыки вождения, и знание конкретной машины. Так и здесь: сначала разбираемся, как работает сеть, затем осваиваем инструменты вроде TensorFlow.",
    "projects": "Формулы автор объясняет через аналогии. После вводных глав читатель строит модели на практике и видит, когда и зачем нужны отдельные инструменты.",
    "milestones": "Глава 2 знакомит с основными понятиями. В начале главы 3 простая сеть выдаёт первый прогноз. Затем читатель повторяет короткий фрагмент кода и к середине главы 4 меняет вес, чтобы уменьшить ошибку.",
    "setup": "На старте нужны основы Python и школьная алгебра, включая чтение графиков. Jupyter Notebook позволяет проверять промежуточные результаты. NumPy упрощает вычисления с массивами и матрицами. Примеры писались на Python 2.7 и проверялись на Python 3.",
    "project": "Траск советует выбрать свою задачу прогнозирования. Его заинтересовала возможность предсказывать биржевые котировки по сообщениям в Twitter."
}
W, H = A4
MARGIN = 56
CONTENT = W - MARGIN * 2

pdf = Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
pdf.setTitle("Грокаем глубокое обучение. Глава 1")
pdf.setSubject("Конспект первой главы книги Эндрю Траска")
pdf.setAuthor("Конспект по книге Эндрю Траска")


def label(text, x, y, size=10, color=MUTED, font="SegoeSemibold"):
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    pdf.drawString(x, H - y, text)


def right_label(text, x, y, size=10, color=MUTED, font="SegoeSemibold"):
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    pdf.drawRightString(x, H - y, text)


def para(text, x, y, width=CONTENT, size=12.7, leading=17.5, color=INK, font="Segoe"):
    style = ParagraphStyle(
        "chapter",
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
    )
    block = Paragraph(text, style)
    _, height = block.wrap(width, H)
    block.drawOn(pdf, x, H - y - height)
    return y + height


def line(x1, x2, y, color=RULE):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(0.75)
    pdf.line(x1, H - y, x2, H - y)


def rect(x, y, width, height, color):
    pdf.setFillColor(color)
    pdf.rect(x, H - y - height, width, height, stroke=0, fill=1)


def heading(text, y):
    label(text, MARGIN, y, 24, INK, "Georgia")


def page(number):
    rect(0, 0, W, H, PAPER)
    label("ЭНДРЮ ТРАСК  /  ГРОКАЕМ ГЛУБОКОЕ ОБУЧЕНИЕ", MARGIN, 57)
    right_label("ГЛАВА 1", W - MARGIN, 57)
    line(MARGIN, W - MARGIN, 70)
    line(MARGIN, W - MARGIN, 777)
    label("КОНСПЕКТ ГЛАВЫ", MARGIN, 802)
    right_label(f"{number} / 2", W - MARGIN, 802)


def link(text, url, x, y):
    label(text, x, y, 10.2, ACCENT)
    width = pdfmetrics.stringWidth(text, "SegoeSemibold", 10.2)
    line(x, x + width, y + 2.5, ACCENT)
    pdf.linkURL(url, (x, H - y - 3, x + width, H - y + 11), relative=0)


page(1)
pdf.bookmarkPage("chapter-one")
pdf.addOutlineEntry("Глава 1. Введение в глубокое обучение", "chapter-one")
label("Введение в", MARGIN, 125, 41, INK, "Georgia")
label("глубокое обучение", MARGIN, 171, 41, INK, "Georgia")
label("Зачем его изучать", MARGIN + 2, 204, 21, ACCENT, "GeorgiaItalic")

rect(MARGIN, 224, CONTENT, 106, TINT)
label("ГЛАВНАЯ МЫСЛЬ", MARGIN + 19, 247, 10, ACCENT)
idea_end = para(COPY["idea"], MARGIN + 19, 256, CONTENT - 38, 15.5, 20.5, ACCENT, "Georgia")
assert idea_end < 325

heading("Зачем изучать глубокое обучение", 364)
y = para(COPY["applications"], MARGIN, 377)
y = para(COPY["automation"], MARGIN, y + 10)
y = para(COPY["creative"], MARGIN, y + 10)

line(MARGIN, W - MARGIN, y + 17)
heading("Как устроена книга", y + 48)
y = para(COPY["framework"], MARGIN, y + 62)
y = para(COPY["projects"], MARGIN, y + 10)
y = para(COPY["milestones"], MARGIN, y + 10)
assert y < 763, y
pdf.showPage()

page(2)
heading("Что нужно для старта", 117)
y = para(COPY["setup"], MARGIN, 132)
y = para(COPY["project"], MARGIN, y + 14)

example_top = y + 28
rect(MARGIN, example_top, CONTENT, 315, TINT)
inset = MARGIN + 22
example_width = CONTENT - 44
label("УЧЕБНЫЙ ПРИМЕР К КОНСПЕКТУ", inset, example_top + 28, 9.8, ACCENT)
label("Сколько займёт дорога?", inset, example_top + 62, 23, INK, "Georgia")
y = para(
    "Допустим, три последние поездки заняли 32, 40 и 36 минут. "
    "Возьмём их среднее как первый прогноз. Следующая поездка заняла 44 минуты.",
    inset, example_top + 75, example_width,
)
line(inset, inset + example_width, y + 15)
label("Прогноз", inset, y + 41, 11.5, ACCENT)
label("(32 + 40 + 36) / 3 = 36 минут", inset + 112, y + 41, 13, INK, "Segoe")
line(inset, inset + example_width, y + 53)
label("Величина ошибки", inset, y + 79, 11.5, ACCENT)
label("44 − 36 = 8 минут", inset + 112, y + 79, 13, INK, "Segoe")
line(inset, inset + example_width, y + 91)
y = para(
    "Чтобы проверить, можно ли прогнозировать точнее, начни записывать день недели, "
    "погоду и время выезда. Сравни новый способ с простым средним на следующих поездках.",
    inset, y + 107, example_width,
)
assert y < example_top + 303

y = example_top + 350
label("ИСТОЧНИКИ", MARGIN, y, 9.5)
link("Глава 1 Manning (с. 3-8)", MANNING, MARGIN, y + 22)
link("Оглавление «Питера» (с. 20-26)", PITER, MARGIN + 164, y + 22)
assert y + 22 < 764
pdf.showPage()
pdf.save()
