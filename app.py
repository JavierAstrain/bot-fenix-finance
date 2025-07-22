import streamlit as st
import pandas as pd
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🧠 Configurar OpenAI API
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📊 Conectar con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(credentials)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1mXxUmIQ44rd9escHOee2w0LxGs4MVNXaPrUeqj4USpk/edit").sheet1
data = pd.DataFrame(sheet.get_all_records())

# 🌐 Interfaz
st.set_page_config(page_title="Fénix Controller IA", page_icon="📊")
st.title("📊 Fénix Controller IA")
st.write("Hola 👋, soy tu analista financiero inteligente. Hazme preguntas como:")
st.markdown("- ¿Cuál fue el total de ingresos en mayo?\n- ¿Cuánto se gastó en pintura?\n- ¿Cuál es el margen promedio?")

# 📥 Entrada del usuario
query = st.text_input("Escribe tu pregunta:")

if query:
    with st.spinner("Pensando... 💭"):
        prompt = f"""
Eres un analista financiero experto que solo responde usando esta tabla:\n{data.to_csv(index=False)}

Pregunta del usuario: {query}
Respuesta:"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Responde como un analista financiero profesional, claro, preciso y amable."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(response["choices"][0]["message"]["content"])
        except Exception as e:
            st.error(f"Error al consultar OpenAI: {e}")
