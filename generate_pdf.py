"""Generate docs/documentation.pdf using ReportLab."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Preformatted, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

os.makedirs("docs", exist_ok=True)

# ── Colour palette ────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#0f4c81")
BLUE   = colors.HexColor("#1a5c99")
LBLUE  = colors.HexColor("#cce0f5")
BG     = colors.HexColor("#f4f6f8")
STRIPE = colors.HexColor("#eef3f9")
WHITE  = colors.white
BLACK  = colors.HexColor("#1a1a1a")
GREY   = colors.HexColor("#888888")

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

S = {
    "title":    style("title",   "Title",   fontSize=24, textColor=NAVY,
                      spaceAfter=6, alignment=TA_CENTER),
    "subtitle": style("sub",     "Normal",  fontSize=11, textColor=BLUE,
                      spaceAfter=18, alignment=TA_CENTER),
    "h2":       style("h2",      "Heading2",fontSize=14, textColor=NAVY,
                      spaceBefore=18, spaceAfter=6),
    "h3":       style("h3",      "Heading3",fontSize=11, textColor=BLUE,
                      spaceBefore=10, spaceAfter=4),
    "body":     style("body",    "Normal",  fontSize=10, leading=15,
                      textColor=BLACK, spaceAfter=6),
    "bullet":   style("bullet",  "Normal",  fontSize=10, leading=15,
                      leftIndent=14, bulletIndent=4, textColor=BLACK,
                      spaceAfter=3),
    "code":     style("code",    "Code",    fontSize=8.5, leading=13,
                      backColor=BG, leftIndent=10, rightIndent=10,
                      fontName="Courier", textColor=colors.HexColor("#2d2d2d")),
    "caption":  style("caption", "Normal",  fontSize=8, textColor=GREY,
                      spaceAfter=4),
    "toc_item": style("toc",     "Normal",  fontSize=10, textColor=BLUE,
                      spaceAfter=2, leftIndent=10),
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def H2(text):
    return [Paragraph(text, S["h2"]),
            HRFlowable(width="100%", thickness=1.2, color=LBLUE, spaceAfter=6)]

def H3(text):
    return [Paragraph(text, S["h3"])]

def P(text):
    return Paragraph(text, S["body"])

def B(text):
    return Paragraph(f"• {text}", S["bullet"])

def Code(text):
    return [Preformatted(text, S["code"]), Spacer(1, 6)]

def HR():
    return HRFlowable(width="100%", thickness=0.5, color=LBLUE,
                      spaceBefore=8, spaceAfter=8)

def tbl(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    cmds = [
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, STRIPE]),
        ("GRID",        (0,0), (-1,-1), 0.4, LBLUE),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]
    if header:
        cmds += [
            ("BACKGROUND",  (0,0), (-1,0), NAVY),
            ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
            ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ]
    t.setStyle(TableStyle(cmds))
    return t

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "docs/documentation.pdf",
    pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2*cm,    bottomMargin=2*cm,
    title="Multilingual Text Preprocessor — Documentation",
    author="text-preprocessor",
)

story = []

# ── Cover ─────────────────────────────────────────────────────────────────────
story += [
    Spacer(1, 2*cm),
    Paragraph("Multilingual Text Preprocessor", S["title"]),
    Paragraph("Technical Documentation  ·  v1.0", S["subtitle"]),
    HR(),
    Spacer(1, 0.4*cm),
]

# Table of Contents (static)
toc_items = [
    "1.  Overview",
    "2.  Project Structure",
    "3.  API Reference",
    "4.  Preprocessing Options",
    "5.  English Pipeline",
    "6.  Arabic Pipeline",
    "7.  Error Handling",
    "8.  Running Locally",
    "9.  Docker Deployment",
    "10. Dependencies",
]
story.append(Paragraph("<b>Table of Contents</b>", S["body"]))
story.append(Spacer(1, 4))
for item in toc_items:
    story.append(Paragraph(item, S["toc_item"]))
story.append(PageBreak())

# ── 1. Overview ───────────────────────────────────────────────────────────────
story += H2("1. Overview")
story.append(P(
    "The Multilingual Text Preprocessor is a modular REST API that cleans and "
    "normalises English and Arabic text through a configurable, per-request "
    "pipeline. It ships with a browser-based GUI, a Swagger UI, and a Docker "
    "image ready for deployment on Hugging Face Spaces or any container host."
))
story.append(Spacer(1, 6))

feat_data = [
    ["Feature", "English", "Arabic"],
    ["Lowercase normalisation", "✓", "—"],
    ["Repeated character normalisation", "✓", "✓"],
    ["URL removal", "✓", "✓"],
    ["Emoji removal", "✓", "✓"],
    ["Punctuation removal", "✓", "✓  (incl. ؟ ، ؛)"],
    ["Number removal", "✓", "✓  (incl. ٠–٩)"],
    ["Stopword removal", "✓", "✓  (negations protected)"],
    ["Stemming", "✓  Porter", "✓  ISRI"],
    ["Lemmatisation", "✓  WordNet", "—"],
    ["Tashkeel (diacritics) removal", "—", "✓"],
    ["Tatweel removal", "—", "✓"],
    ["Alef normalisation (أ إ آ → ا)", "—", "✓"],
    ["Ya normalisation (ى → ي)", "—", "✓"],
    ["Web GUI", "✓", "✓"],
    ["Swagger UI  (/docs)", "✓", "✓"],
]
story.append(tbl(feat_data, [8.5*cm, 3.5*cm, 4.5*cm]))
story.append(Spacer(1, 10))

# ── 2. Project Structure ──────────────────────────────────────────────────────
story += H2("2. Project Structure")
story += Code("""\
text-preprocessor/
├── Dockerfile
├── requirements.txt
├── static/
│   └── index.html                  # Web GUI
└── src/
    ├── main.py                     # FastAPI app, routes, error handlers
    ├── models/
    │   └── schemas.py              # Pydantic request / response models
    ├── routers/
    │   └── preprocess.py           # POST /api/preprocess endpoint
    ├── services/
    │   ├── pipeline.py             # Language routing
    │   ├── english_processor.py
    │   └── arabic_processor.py
    └── utils/
        ├── cleaning.py             # Language-agnostic utilities
        ├── arabic_cleaning.py      # Arabic-specific utilities
        └── exceptions.py          # Custom exception hierarchy""")

# ── 3. API Reference ──────────────────────────────────────────────────────────
story += H2("3. API Reference")
story += H3("POST  /api/preprocess")
story.append(P("Preprocesses text according to the supplied options. All option fields default to <i>false</i>."))
story.append(Spacer(1, 4))

story += H3("Request body (JSON)")
story += Code("""\
{
  "text":     "The students are Runninggg!! Visit https://example.com 😊",
  "language": "en",
  "options": {
    "normalize":          true,
    "remove_urls":        true,
    "remove_emojis":      true,
    "remove_punctuation": true,
    "remove_numbers":     false,
    "remove_stopwords":   true,
    "stemming":           false,
    "lemmatize":          true
  }
}""")

req_data = [
    ["Field", "Type", "Required", "Description"],
    ["text", "string", "Yes", "Input text to process"],
    ["language", '"en" | "ar"', "Yes", "Language code"],
    ["options", "object", "Yes", "Preprocessing flags (all default false)"],
]
story.append(tbl(req_data, [3*cm, 3.2*cm, 2.3*cm, 8*cm]))
story.append(Spacer(1, 10))

story += H3("Response body (JSON)")
story += Code("""\
{
  "original_text":  "The students are Runninggg!! Visit https://example.com 😊",
  "processed_text": "student run",
  "language":       "en",
  "applied_steps":  [
    "lowercase", "normalize_repeated_chars", "remove_urls",
    "remove_emojis", "remove_punctuation", "remove_stopwords", "lemmatize"
  ]
}""")

resp_data = [
    ["Field", "Type", "Description"],
    ["original_text",  "string",   "The unmodified input text"],
    ["processed_text", "string",   "Text after all pipeline steps"],
    ["language",       "string",   "Language code used"],
    ["applied_steps",  "string[]", "Ordered list of steps that ran"],
]
story.append(tbl(resp_data, [3.8*cm, 2.8*cm, 9.9*cm]))
story.append(Spacer(1, 10))

story += H3("Error responses")
err_data = [
    ["HTTP Status", "Condition"],
    ["400", "Unsupported language code"],
    ["422", "Text is empty after processing"],
    ["500", "NLP resource failed to load"],
]
story.append(tbl(err_data, [3.5*cm, 13*cm]))

# ── 4. Preprocessing Options ──────────────────────────────────────────────────
story.append(PageBreak())
story += H2("4. Preprocessing Options")
opt_data = [
    ["Option", "Default", "Description"],
    ["normalize",          "false", "Lowercase (EN) + repeated-char normalisation + Arabic script normalisation (AR)"],
    ["remove_urls",        "false", "Strip http://, https://, and www. URLs"],
    ["remove_emojis",      "false", "Remove emoji and Unicode symbol characters"],
    ["remove_punctuation", "false", "Remove punctuation, including Arabic ؟ ، ؛ « »"],
    ["remove_numbers",     "false", "Remove digit sequences (0–9 and Arabic-Indic ٠–٩)"],
    ["remove_stopwords",   "false", "Remove stopwords; Arabic negations are preserved"],
    ["stemming",           "false", "Porter stemmer (EN) / ISRI stemmer (AR)"],
    ["lemmatize",          "false", "WordNet lemmatisation — English only"],
]
story.append(tbl(opt_data, [4.2*cm, 2*cm, 10.3*cm]))

# ── 5. English Pipeline ───────────────────────────────────────────────────────
story.append(Spacer(1, 12))
story += H2("5. English Pipeline")
story.append(P("Steps execute in the fixed order below. A step runs only when its option is enabled."))
story.append(Spacer(1, 4))

en_steps = [
    ["Step", "Option", "Action"],
    ["1", "normalize",          "Lowercase the text"],
    ["2", "normalize",          "Cap repeated characters at 2  (soooo → soo)"],
    ["3", "remove_urls",        "Strip http(s):// and www. URLs"],
    ["4", "remove_emojis",      "Strip emoji / Unicode symbol characters"],
    ["5", "remove_punctuation", "Strip # symbols then all punctuation"],
    ["6", "remove_numbers",     "Strip digit sequences"],
    ["7", "(always)",           "Tokenise with NLTK word_tokenize"],
    ["8", "remove_stopwords",   "Filter NLTK English stopword list"],
    ["9", "stemming",           "Apply Porter stemmer to each token"],
    ["10","lemmatize",          "Apply WordNet lemmatiser to each token"],
    ["11","(always)",           "Re-join tokens; collapse whitespace"],
]
story.append(tbl(en_steps, [1.5*cm, 4*cm, 11*cm]))
story.append(Spacer(1, 10))

story += H3("Example")
story += Code("""\
Input:   "The students are Runninggg quickly!! Visit https://example.com 😊"
Options: normalize, remove_urls, remove_emojis, remove_punctuation,
         remove_stopwords, lemmatize

Output:  "student run quickly"
Steps:   lowercase → normalize_repeated_chars → remove_urls → remove_emojis
         → remove_punctuation → remove_stopwords → lemmatize""")

# ── 6. Arabic Pipeline ────────────────────────────────────────────────────────
story.append(PageBreak())
story += H2("6. Arabic Pipeline")
story.append(P("Steps execute in the fixed order below. A step runs only when its option is enabled."))
story.append(Spacer(1, 4))

ar_steps = [
    ["Step", "Option", "Action"],
    ["1", "normalize", "Remove tashkeel (diacritics: fatha, damma, kasra …)"],
    ["2", "normalize", "Remove tatweel (stretching character ـ)"],
    ["3", "normalize", "Normalise alef variants: أ إ آ → ا"],
    ["4", "normalize", "Normalise ya: ى → ي"],
    ["5", "normalize", "Cap repeated characters at 2"],
    ["6", "remove_urls",        "Strip URLs"],
    ["7", "remove_emojis",      "Strip emoji / Unicode symbol characters"],
    ["8", "remove_punctuation", "Strip punctuation incl. Arabic ؟ ، ؛ « »"],
    ["9", "remove_numbers",     "Strip digits (0–9 and ٠–٩)"],
    ["10","(always)",           "Tokenise by whitespace"],
    ["11","remove_stopwords",   "Filter NLTK Arabic stopwords (negations kept)"],
    ["12","stemming",           "Apply ISRI stemmer to each token"],
    ["13","(always)",           "Re-join tokens; collapse whitespace"],
]
story.append(tbl(ar_steps, [1.5*cm, 4*cm, 11*cm]))
story.append(Spacer(1, 10))

story += H3("Protected Arabic negations")
story.append(P(
    "The following words are removed from the stopword list before filtering, "
    "so they are never deleted even when <i>remove_stopwords</i> is enabled:"
))
for w in ["لا", "ليس", "ليست", "لم", "لن", "ما", "غير"]:
    story.append(B(w))
story.append(Spacer(1, 8))

story += H3("Example — full pipeline")
story += Code("""\
Input:   "الطُّلابُ يَدرُسُونَ فِي الجَامِعَةِ!! العدد ١٢٣"
Options: normalize, remove_punctuation, remove_numbers, remove_stopwords

Output:  "طلاب يدرسون جامعه"
Steps:   remove_tashkeel → remove_tatweel → normalize_alef → normalize_ya
         → normalize_repeated_chars → remove_punctuation
         → remove_numbers → remove_stopwords_safe""")

story += H3("Example — negation preservation")
story += Code("""\
Input:   "هذا المنتج ليس جيداً"
Options: normalize, remove_stopwords

Output:  "المنتج ليس جيدا"   ← "ليس" is preserved""")

# ── 7. Error Handling ─────────────────────────────────────────────────────────
story += H2("7. Error Handling")
story.append(P("All custom errors extend <b>PreprocessingError</b> and return a JSON body:"))
story += Code("""\
{ "detail": "<human-readable message>" }""")

exc_data = [
    ["Exception class", "HTTP", "Trigger"],
    ["UnsupportedLanguageError", "400", 'Language code is not "en" or "ar"'],
    ["EmptyTextError",           "422", "Text is empty after all processing steps"],
    ["NLPResourceError",         "500", "An NLTK resource failed to load"],
]
story.append(tbl(exc_data, [5.5*cm, 2*cm, 9*cm]))

# ── 8. Running Locally ────────────────────────────────────────────────────────
story.append(PageBreak())
story += H2("8. Running Locally")
story.append(P("<b>Requirements:</b> Python 3.10+"))
story += Code("""\
# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload""")

story.append(P("Open the web GUI:   <b>http://localhost:8000</b>"))
story.append(P("Swagger UI:         <b>http://localhost:8000/docs</b>"))

# ── 9. Docker Deployment ──────────────────────────────────────────────────────
story += H2("9. Docker Deployment")
story += Code("""\
# Build the image
docker build -t text-preprocessor .

# Run the container
docker run -p 7860:7860 text-preprocessor""")

story.append(P("Open the web GUI:   <b>http://localhost:7860</b>"))
story.append(P("Swagger UI:         <b>http://localhost:7860/docs</b>"))
story.append(Spacer(1, 6))
story.append(P(
    "The container respects a <b>PORT</b> environment variable and defaults to "
    "<b>7860</b>. The Hugging Face Spaces deployment uses this default."
))

# ── 10. Dependencies ──────────────────────────────────────────────────────────
story += H2("10. Dependencies")
dep_data = [
    ["Package", "Version", "Purpose"],
    ["fastapi",   "0.115.0", "Web framework"],
    ["uvicorn",   "0.30.6",  "ASGI server"],
    ["pydantic",  "2.9.0",   "Request / response validation"],
    ["nltk",      "3.9.1",   "Tokenisation, stopwords, stemming, lemmatisation"],
    ["pyarabic",  "0.6.15",  "Arabic text utilities"],
]
story.append(tbl(dep_data, [3.2*cm, 2.8*cm, 10.5*cm]))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
size_kb = os.path.getsize("docs/documentation.pdf") // 1024
print(f"Created: docs/documentation.pdf  ({size_kb} KB)")
