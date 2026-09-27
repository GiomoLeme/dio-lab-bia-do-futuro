import json

import pandas as pd
import requests
import streamlit as st


# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"


# ============ CARREGAR DADOS ============
with open("./data/perfil_investidor.json", encoding="utf-8") as arquivo:
    perfil = json.load(arquivo)

transacoes = pd.read_csv("./data/transacoes.csv")
historico = pd.read_csv("./data/historico_atendimento.csv")

with open("./data/produtos_financeiros.json", encoding="utf-8") as arquivo:
    produtos = json.load(arquivo)


# ============ MONTAR CONTEXTO ============
contexto = f"""
PERFIL DO CLIENTE:
{json.dumps(perfil, indent=2, ensure_ascii=False)}

TRANSAÇÕES:
{transacoes.to_string(index=False)}

HISTÓRICO DE ATENDIMENTO:
{historico.to_string(index=False)}

PRODUTOS FINANCEIROS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""


# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o FinEdu, um assistente educativo de finanças pessoais.
Seu objetivo é explicar conceitos financeiros de forma simples, paciente e não julgadora, usando os dados fictícios fornecidos como contexto.

REGRAS:
- Nunca recomende investimentos específicos. Explique apenas como os produtos funcionam, seus riscos e características.
- Quando a pergunta depender de dados do cliente, transações, atendimentos ou produtos, use somente o contexto fornecido.
- Nunca invente valores, taxas, produtos, transações ou informações financeiras.
- Se a informação não estiver disponível, diga claramente que não possui essa informação.
- Não responda perguntas fora do tema de educação financeira.
- Não forneça nem solicite senhas ou outras informações sensíveis.
- Responda com linguagem simples, de forma curta e direta, em no máximo 3 parágrafos.
"""


# ============ CHAMAR OLLAMA ============
def perguntar(mensagem):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO:
{contexto}

PERGUNTA DO USUÁRIO:
{mensagem}
"""

    try:
        resposta = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resposta.raise_for_status()
        return resposta.json()["response"]
    except requests.RequestException:
        return (
            "Não foi possível conectar ao Ollama. Verifique se ele está instalado, "
            "se o modelo foi baixado e se o comando 'ollama serve' está em execução."
        )


# ============ INTERFACE ============
st.title("💰 FinEdu")
st.write("Seu assistente de educação financeira.")
st.caption(
    "Esta aplicação usa dados fictícios e oferece conteúdo educativo. "
    "Ela não recomenda investimentos."
)

if pergunta_usuario := st.chat_input("Digite sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta_usuario)

    with st.spinner("Preparando uma explicação..."):
        resposta_fin_edu = perguntar(pergunta_usuario)

    st.chat_message("assistant").write(resposta_fin_edu)
