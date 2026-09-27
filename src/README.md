# Execução da aplicação

Todo o código do FinEdu está em `src/app.py`.

Na raiz do projeto, execute:

```bash
pip install streamlit pandas requests
ollama pull gpt-oss
ollama serve
```

Em outro terminal, também na raiz do projeto:

```bash
streamlit run src/app.py
```

Os quatro arquivos da pasta `data/` contêm somente dados fictícios fornecidos pela DIO.
