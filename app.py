import os
from datetime import datetime

import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


# ==================== CONFIGURAÇÃO STREAMLIT ====================
st.set_page_config(
    page_title="ATS Shield | Resume Architect",
    page_icon="🎯",
    layout="wide"
)

# Carrega .env local se existir
load_dotenv(find_dotenv(), override=True)

OUTPUT_DIR = "curriculos_gerados"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_openai_api_key():
    api_key = None

    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    return api_key


OPENAI_API_KEY = get_openai_api_key()


# --- CSS CUSTOMIZADO PARA VISUAL PROFISSIONAL ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }

    div.stButton > button:first-child {
        background-color: #003366;
        color: white;
        border-radius: 8px;
        border: none;
        height: 3rem;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #004a94;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .history-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #003366;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    .stTextArea textarea, .stTextInput input {
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== LÓGICA DE EXTRAÇÃO E IA ====================

def extrair_texto_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    textos = []

    for page in reader.pages:
        texto = page.extract_text()
        if texto:
            textos.append(texto)

    return "\n".join(textos)


def gerar_conteudo_ia(curriculo_base, vaga):
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.15,
        api_key=OPENAI_API_KEY
    )

    prompt_template = """
Você é um especialista em recrutamento Tech.
Otimize o currículo abaixo para a vaga fornecida.

INSTRUÇÕES:
- O Cargo de interesse DEVE ser: "Analista de Sistemas Júnior | RPA e IA".
- Na FORMAÇÃO, SEMPRE inclua: "MBA em AI Engineering & Multi-Agents - FIAP (Início: 09/2024)".
- Melhore os textos usando o método XYZ (Fiz X, medido por Y, resultando em Z).
- MANTENHA as competências técnicas originais.
- OBRIGATÓRIO: Inclua a seção de projetos relevantes detalhadamente.
- Remova TODAS as datas de experiências profissionais.

CURRÍCULO:
{curriculo_base}

VAGA:
{vaga}

Retorne APENAS um JSON válido no formato:
{{
  "titulo_profissional": "Analista de Sistemas Júnior | RPA e IA",
  "resumo_profissional": "string",
  "experiencia_profissional": [
    {{
      "cargo": "string",
      "empresa": "string",
      "bullets": ["string", "string"]
    }}
  ],
  "projetos_relevantes": [
    {{
      "nome": "string",
      "descricao": "string",
      "tecnologias": ["string", "string"]
    }}
  ],
  "competencias_tecnicas": {{
    "Categoria": ["Skill", "Skill"]
  }},
  "formacao": [
    {{
      "curso": "MBA em AI Engineering & Multi-Agents",
      "instituicao": "FIAP",
      "status": "Em andamento (Início: 09/2024)"
    }},
    {{
      "curso": "Análise e Desenvolvimento de Sistemas",
      "instituicao": "Cruzeiro do Sul",
      "status": "Concluído"
    }}
  ]
}}
"""

    prompt = PromptTemplate.from_template(prompt_template)
    parser = JsonOutputParser()
    chain = prompt | llm | parser

    return chain.invoke({
        "curriculo_base": curriculo_base,
        "vaga": vaga
    })


# ==================== LÓGICA DO PDF ====================

def criar_pdf_file(dados, nome_arquivo):
    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm
    )

    color_primary = HexColor("#003366")
    color_text = HexColor("#333333")
    styles = getSampleStyleSheet()

    def update_style(name, **kwargs):
        if name in styles.byName:
            for k, v in kwargs.items():
                setattr(styles[name], k, v)
        else:
            styles.add(ParagraphStyle(name=name, parent=styles["Normal"], **kwargs))

    update_style(
        "HeaderName",
        fontSize=22,
        fontName="Helvetica-Bold",
        textColor=color_primary,
        alignment=TA_CENTER,
        leading=28
    )
    update_style(
        "HeaderTitle",
        fontSize=11,
        fontName="Helvetica",
        textColor=color_text,
        alignment=TA_CENTER
    )
    update_style(
        "HeaderContact",
        fontSize=8,
        fontName="Helvetica",
        textColor=color_text,
        alignment=TA_CENTER
    )
    update_style(
        "SectionTitle",
        fontSize=11,
        fontName="Helvetica-Bold",
        textColor=color_primary,
        spaceBefore=12,
        spaceAfter=4
    )
    update_style(
        "BodyText",
        fontSize=9.5,
        fontName="Helvetica",
        textColor=color_text,
        alignment=TA_JUSTIFY,
        leading=12
    )
    update_style(
        "BulletItem",
        fontSize=9.5,
        fontName="Helvetica",
        textColor=color_text,
        leftIndent=5 * mm,
        leading=12,
        spaceAfter=2
    )

    story = []

    story.append(Paragraph("GUSTAVO DE ALENCAR MARINHO NERI", styles["HeaderName"]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("ANALISTA DE SISTEMAS JÚNIOR | RPA E IA", styles["HeaderTitle"]))
    story.append(Spacer(1, 2 * mm))

    contato = (
        "gustavoneri448@gmail.com | (11) 97029-9201 | "
        "github.com/GustavoNer1 | LinkedIn: gustavo-neri-a91305390"
    )
    story.append(Paragraph(contato, styles["HeaderContact"]))
    story.append(Spacer(1, 4 * mm))

    def add_section(title):
        story.append(Paragraph(title, styles["SectionTitle"]))
        story.append(HRFlowable(width="100%", thickness=1, color=color_primary, spaceAfter=4))

    add_section("Resumo Executivo")
    story.append(Paragraph(dados.get("resumo_profissional", ""), styles["BodyText"]))

    add_section("Experiência Profissional")
    for exp in dados.get("experiencia_profissional", []):
        cargo = exp.get("cargo", "")
        empresa = exp.get("empresa", "")
        story.append(Paragraph(f"<b>{cargo}</b> | {empresa}", styles["BodyText"]))

        for bullet in exp.get("bullets", []):
            story.append(Paragraph(f"• {bullet}", styles["BulletItem"]))

        story.append(Spacer(1, 2 * mm))

    projetos = dados.get("projetos_relevantes", [])
    if projetos:
        add_section("Projetos Relevantes")
        for proj in projetos:
            nome = proj.get("nome", "")
            descricao = proj.get("descricao", "")
            tecnologias = proj.get("tecnologias", [])

            story.append(Paragraph(f"<b>{nome}</b>", styles["BodyText"]))
            story.append(Paragraph(descricao, styles["BodyText"]))

            if tecnologias:
                story.append(
                    Paragraph(
                        f"<i>Tecnologias: {', '.join(tecnologias)}</i>",
                        styles["BodyText"]
                    )
                )

            story.append(Spacer(1, 3 * mm))

    add_section("Competências Técnicas")
    for categoria, skills in dados.get("competencias_tecnicas", {}).items():
        story.append(
            Paragraph(f"<b>{categoria}:</b> {' • '.join(skills)}", styles["BodyText"])
        )

    add_section("Formação Acadêmica")
    for form in dados.get("formacao", []):
        curso = form.get("curso", "")
        instituicao = form.get("instituicao", "")
        status = form.get("status", "")
        story.append(
            Paragraph(
                f"<b>{curso}</b> — {instituicao} ({status})",
                styles["BodyText"]
            )
        )

    doc.build(story)
    return nome_arquivo


# ==================== VALIDAÇÃO DA API KEY ====================

if not OPENAI_API_KEY:
    st.error(
        "❌ OPENAI_API_KEY não encontrada. Configure em `.streamlit/secrets.toml` "
        "ou no arquivo `.env`."
    )
    st.stop()


# ==================== INTERFACE STREAMLIT ====================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2808/2808148.png", width=100)
    st.title("ATS Shield")
    st.markdown("---")
    st.info(
        """**Dica Profissional:**  
A IA utiliza o método **XYZ** para descrever suas experiências, o que aumenta as chances de aprovação em sistemas de triagem automática."""
    )
    st.markdown("---")
    st.caption("Desenvolvido por Gustavo Neri")

st.title("👔 Resume Designer Pro")
st.subheader("Otimize seu currículo com Inteligência Artificial")

tab1, tab2 = st.tabs(["🚀 Gerar Novo Currículo", "📂 Histórico de Versões"])

with tab1:
    col_input, col_info = st.columns([2, 1])

    with col_input:
        st.markdown("### 1. Configurações e Arquivo")
        c1, c2 = st.columns(2)

        uploaded_pdf = c1.file_uploader(
            "Currículo Base (PDF)",
            type="pdf",
            help="Seu currículo atual"
        )

        out_name = c2.text_input(
            "Nome do arquivo final",
            value="Curriculo_Neri_RPA_IA",
            help="Como o arquivo será salvo"
        )

        vaga_desc = st.text_area(
            "### 2. Contexto da Vaga\nDescrição da Vaga",
            height=250,
            placeholder="Cole aqui os requisitos e responsabilidades da vaga alvo..."
        )

        if st.button("GERAR CURRÍCULO AGORA"):
            if uploaded_pdf and vaga_desc.strip():
                with st.spinner("🚀 IA analisando vaga e formatando PDF Premium..."):
                    try:
                        base_text = extrair_texto_pdf(uploaded_pdf)
                        json_result = gerar_conteudo_ia(base_text, vaga_desc)

                        nome_final = out_name.strip() or "curriculo_otimizado"
                        pdf_path = os.path.join(OUTPUT_DIR, f"{nome_final}.pdf")

                        criar_pdf_file(json_result, pdf_path)

                        st.balloons()
                        st.success("✨ Currículo gerado e otimizado com sucesso!")

                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 BAIXAR PDF OTIMIZADO",
                                data=f,
                                file_name=f"{nome_final}.pdf",
                                mime="application/pdf"
                            )

                    except Exception as e:
                        st.error(f"❌ Erro no processamento: {e}")
            else:
                st.warning("⚠️ Por favor, suba seu PDF base e cole a descrição da vaga.")

    with col_info:
        st.markdown("### ✨ O que acontece?")
        st.write("1. **Parsing:** Extraímos o texto do seu PDF.")
        st.write("2. **Mapping:** A IA mapeia suas habilidades para os termos da vaga.")
        st.write("3. **XYZ Style:** As conquistas são reescritas com foco em métricas.")
        st.write("4. **PDF Render:** Um arquivo novo é gerado com layout Anti-ATS.")

with tab2:
    st.markdown("### 📂 Meus Currículos Gerados")
    files = sorted(os.listdir(OUTPUT_DIR), reverse=True)

    if not files:
        st.info("Nenhum currículo gerado ainda.")
    else:
        for f in files:
            caminho = os.path.join(OUTPUT_DIR, f)
            data_criacao = datetime.fromtimestamp(os.path.getctime(caminho)).strftime("%d/%m/%Y %H:%M")

            st.markdown(
                f"""
                <div class="history-card">
                    <strong>📄 {f}</strong><br>
                    <small>Gerado em: {data_criacao}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

            with open(caminho, "rb") as file_to_dl:
                st.download_button(
                    label=f"Download {f}",
                    data=file_to_dl,
                    file_name=f,
                    key=f"dl_btn_{f}"
                )

            st.markdown("<br>", unsafe_allow_html=True)