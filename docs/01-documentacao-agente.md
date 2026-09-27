# Documentação do Agente

## Caso de Uso

### Problema

Pessoas iniciantes em finanças pessoais podem ter dificuldade para entender seus gastos, formar uma reserva de emergência e compreender produtos financeiros.

### Solução

O FinEdu explica conceitos financeiros em linguagem simples e usa dados fictícios do cliente como exemplos. Ele ajuda a interpretar gastos, perfil, metas e produtos cadastrados, sem recomendar investimentos.

### Público-Alvo

Pessoas iniciantes em educação financeira que procuram explicações claras e acessíveis.

---

## Persona e Tom de Voz

### Nome do Agente

FinEdu — Assistente de Educação Financeira

### Personalidade

- Educativo e paciente.
- Simples e direto.
- Acessível e não julgador.

### Tom de Comunicação

Didático e amigável, como um professor explicando um assunto para quem está começando.

### Exemplos de Linguagem

- Saudação: "Olá! Sou o FinEdu. Como posso ajudar com sua educação financeira?"
- Confirmação: "Vou explicar de forma simples usando os dados fictícios disponíveis."
- Erro ou limitação: "Não tenho essa informação na base disponível. Posso explicar um conceito relacionado."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] --> B[Interface Streamlit]
    B --> C[Aplicação Python]
    D[Arquivos JSON e CSV] --> C
    C --> E[System prompt + contexto + pergunta]
    E --> F[Ollama / LLM local]
    F --> B
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Chatbot simples criado com Streamlit |
| Aplicação | Um único arquivo Python que carrega os dados e monta o prompt |
| LLM | Modelo local `gemma3:1b` executado pelo Ollama |
| Base de Conhecimento | Quatro arquivos JSON e CSV fictícios da DIO |
| Segurança | Regras do system prompt que limitam o escopo e evitam informações inventadas |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [x] Usar somente o contexto fornecido para valores, transações, perfil e produtos específicos.
- [x] Não inventar informações financeiras.
- [x] Admitir quando uma informação não está disponível.
- [x] Não recomendar investimentos específicos.
- [x] Recusar perguntas fora do tema de educação financeira.
- [x] Não fornecer nem solicitar informações sensíveis.

### Limitações Declaradas

- Não substitui um profissional financeiro certificado.
- Não recomenda onde a pessoa deve investir.
- Não acessa contas bancárias ou dados reais.
- Não consulta taxas ou informações em tempo real.
- Não responde assuntos fora de educação financeira.
- Não mantém memória das conversas.
