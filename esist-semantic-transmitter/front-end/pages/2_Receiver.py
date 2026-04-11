import streamlit as st
import json
import os

st.set_page_config(page_title="Receiver", page_icon="📥", layout="wide")

st.title("📥 Interface do Recetor (Equipa 10)")
st.markdown("Aqui vamos apresentar os dados semânticos recebidos e gerar a resposta em áudio!")

# Exemplo de lógica para ler o pacote que o FastAPI vai guardar:
if os.path.exists("ultimo_pacote.json"):
    with open("ultimo_pacote.json", "r", encoding="utf-8") as f:
        pacote = json.load(f)
    
    st.success("Pacote Semântico Detetado!")
    st.json(pacote)
else:
    st.info("À espera de dados do Transmissor... O servidor FastAPI está ligado?")