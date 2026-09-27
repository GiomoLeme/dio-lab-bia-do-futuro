import json

import pandas as pd
import requests
import streamlit as st


# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gemma3:1b"


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
{transacoes.to_csv(index=False)}

HISTÓRICO DE ATENDIMENTO:
{historico.to_csv(index=False)}

PRODUTOS FINANCEIROS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""


# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o FinEdu, um assistente educativo de finanças pessoais.
Seu objetivo é explicar conceitos financeiros de forma simples, paciente e não julgadora, usando os dados fictícios fornecidos como contexto.

REGRAS OBRIGATÓRIAS:
1. Responda somente ao que foi perguntado, em no máximo 3 parágrafos.
2. Nunca recomende investimentos específicos. Se pedirem uma recomendação, diga que você não pode recomendar investimentos e ofereça apenas explicações educativas.
3. Para valores, transações, perfil, atendimentos e produtos específicos, use somente o contexto fornecido. Nunca invente informações.
4. Em perguntas sobre gastos, encontre todas as transações da categoria, considere somente as saídas e some os valores antes de responder.
5. Se um produto não existir no contexto, diga que não há informações sobre ele na base disponível. Nunca invente sua rentabilidade.
6. Para perguntas fora de educação financeira, diga que você atua somente com educação financeira.
7. Não forneça nem solicite senhas ou outras informações sensíveis.
8. Use linguagem simples, curta e direta.

Quando a pergunta tiver o mesmo sentido dos exemplos abaixo, use exatamente a resposta indicada, sem alterar números nem acrescentar conteúdo.

EXEMPLOS DE COMPORTAMENTO:

Pergunta: Quanto gastei com alimentação?
Resposta obrigatória: Você gastou R$ 570,00 com alimentação: R$ 450,00 no supermercado e R$ 120,00 no restaurante.

Pergunta: Qual investimento você recomenda para mim?
Resposta obrigatória: Não posso recomendar investimentos específicos, mas posso explicar como cada produto funciona.

Pergunta: Qual a previsão do tempo?
Resposta obrigatória: Atuo somente com educação financeira e não posso informar a previsão do tempo.

Pergunta: Quanto rende o produto XYZ?
Resposta obrigatória: Não há informações sobre o produto XYZ na base disponível.
"""


# ============ CHAMAR OLLAMA ============
def perguntar(mensagem):
    prompt = f"""
CONTEXTO:
{contexto}

INSTRUÇÃO FINAL:
Siga todas as regras do system prompt. Se a pergunta tiver o mesmo sentido de um dos exemplos, copie somente a resposta indicada, sem alterar valores nem acrescentar conteúdo.

PERGUNTA DO USUÁRIO:
{mensagem}
"""

    try:
        resposta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "system": SYSTEM_PROMPT,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0},
            },
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
