# 📄 AI Resume Architect & ATS Optimizer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)

O **AI Resume Architect** é uma aplicação inteligente desenvolvida para resolver um problema real do mercado de tecnologia: a triagem automatizada de currículos por sistemas ATS (*Applicant Tracking Systems*).

Utilizando o poder do GPT-4o, o sistema analisa a descrição de uma vaga e adapta dinamicamente um currículo base, otimizando palavras-chave, reformulando experiências com foco em métricas e gerando um novo PDF com layout executivo e alta legibilidade.

## 🚀 Principais funcionalidades

- **Extração inteligente:** faz upload de um currículo base em PDF para servir como contexto de entrada.
- **Otimização tailor-made:** reescreve experiências profissionais com o Método XYZ — *Fiz X, medido por Y, resultando em Z*.
- **Foco em IA e RPA:** destaca competências em automação, agentes de IA e engenharia de software.
- **Geração de PDF premium:** cria documentos dinamicamente com ReportLab, seguindo um layout limpo e profissional.
- **Gerenciamento de histórico:** armazena localmente versões geradas para consulta e download posterior.
- **Mobile friendly:** interface responsiva desenvolvida em Streamlit, permitindo o uso direto pelo smartphone.

## 🛠️ Stack tecnológica

- **Linguagem:** Python 3.10+
- **Orquestração LLM:** LangChain
- **Modelo de IA:** OpenAI GPT-4o
- **Front-end:** Streamlit
- **Document Engine:** ReportLab
- **PDF Parsing:** PyPDF2

## 🏗️ Arquitetura do sistema

### 1. Input Layer
O usuário fornece:
- o currículo original em PDF;
- a descrição da vaga alvo.

### 2. Context Extraction
O texto do currículo é extraído do PDF e enviado como contexto para o modelo de linguagem.

### 3. AI Logic
Um prompt estruturado instrui o modelo a retornar um JSON estritamente formatado, garantindo que informações críticas — como formação, experiências e competências técnicas — sejam mantidas e destacadas.

### 4. Rendering Layer
O JSON gerado é processado pelo ReportLab, que monta o currículo com regras de tipografia e espaçamento para evitar sobreposição de elementos.

### 5. Storage
O arquivo final é salvo localmente e disponibilizado para download imediato.

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SeuUsuario/AI-Resume-Architect.git
cd AI-Resume-Architect
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode a aplicação

```bash
streamlit run app.py
```

