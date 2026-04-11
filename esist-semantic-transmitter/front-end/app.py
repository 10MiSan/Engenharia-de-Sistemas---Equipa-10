import streamlit as st

st.set_page_config(page_title="Semantic Comms", page_icon="📡")

st.markdown("""
# 📡 Projeto de Comunicação Semântica
Bem-vindo ao sistema integrado das Equipas 9 e 10.

Por favor, utilize o **menu lateral esquerdo** para escolher o seu modo de operação:

* **Transmitter (Equipa 9):** Captura áudio, extrai semântica e envia o pacote.
* **Receiver (Equipa 10):** Recebe o pacote, lê a semântica e gera a resposta auditiva.
""")