# Base de Conhecimento

## Dados Utilizados

O FinEdu utiliza sem alterações os dados fictícios fornecidos no repositório-base da DIO.

| Arquivo | Formato | Utilização no Agente |
|---------|---------|----------------------|
| `historico_atendimento.csv` | CSV | Contextualizar os temas de atendimentos anteriores |
| `perfil_investidor.json` | JSON | Contextualizar perfil, objetivo e metas do cliente fictício |
| `produtos_financeiros.json` | JSON | Explicar características dos produtos cadastrados, sem recomendá-los |
| `transacoes.csv` | CSV | Responder perguntas sobre gastos, entradas, saídas e categorias |

Não são utilizados dados bancários reais nem datasets externos.

---

## Adaptações nos Dados

Os quatro arquivos foram mantidos como fornecidos pela DIO, sem inclusão, exclusão ou alteração de registros.

---

## Estratégia de Integração

### Como os dados são carregados?

Os arquivos JSON são carregados com a biblioteca nativa `json`. Os arquivos CSV são carregados com Pandas no início da aplicação.

### Como os dados são usados no prompt?

Os dados são convertidos em texto e reunidos em uma única variável de contexto. Esse contexto é combinado com o system prompt e com a pergunta do usuário antes de ser enviado ao Ollama.

Essa estratégia é uma injeção direta de contexto. O projeto não utiliza RAG, embeddings, banco vetorial ou busca externa.

---

## Exemplo de Contexto Montado

```text
PERFIL DO CLIENTE:
{
  "nome": "João Silva",
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência"
}

TRANSAÇÕES:
2025-10-03  Supermercado  alimentacao  450.00  saida
2025-10-10  Restaurante   alimentacao  120.00  saida

HISTÓRICO DE ATENDIMENTO:
2025-10-01  chat  Tesouro Selic  Cliente pediu explicação sobre o funcionamento do Tesouro Direto

PRODUTOS FINANCEIROS:
Tesouro Selic, CDB Liquidez Diária, LCI/LCA, Fundo Multimercado e Fundo de Ações
```

Na aplicação, o contexto contém integralmente os quatro arquivos, e não somente o trecho resumido acima.
