import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(layout="wide")

st.title("Cuentas Bancarias Proveedores")

# Crear conexión a la hoja de cálculo
conn = st.experimental_connection("gsheets", type=GSheetsConnection)
worksheet = "Hoja 1"

# Mostrar el DataFrame actualizado en la aplicación
st.dataframe(conn.read(worksheet=worksheet))


# Agregar un campo de búsqueda en la barra lateral
st.sidebar.header("Buscar en la Hoja de Cálculo")
search_query = st.sidebar.text_input("Buscar (RUT o TITULAR)").lower()

# Filtrar el DataFrame basado en la consulta de búsqueda
if search_query:
    filtered_df = conn.read(worksheet=worksheet)
    filtered_df = filtered_df[filtered_df["RUT Completo"].str.contains(search_query) | filtered_df["TITULAR"].str.lower().str.contains(search_query)]
    st.dataframe(filtered_df)

# Formulario para ingresar datos de Cuenta Bancaria en la barra lateral
with st.sidebar.form("Datos de Cuenta Bancaria"):
    rut = st.text_input("RUT")
    digito = st.selectbox("Digito Verificador", ["","1", "2", "3", "4", "5", "6", "7", "8", "9", "K"])
    titular = st.text_input("TITULAR")
    banco = st.selectbox("BANCO", ["", "BBVA", "BCI", "BICE", "CHILE", "CONSORCIO", "ESTADO", "FALABELLA", "INTERNACIONAL", "ITAU", "RIPLEY", "SANTANDER", "SCOTIABANK", "SECURITY", "COOPEUCH", "HSBC", "CORP BANCA", "VALE VISTA"])
    codigo_banco = st.selectbox("Cod. Banco", ["", "1", "9", "12", "14", "16", "27", "28", "31", "37", "39", "49", "51", "53", "55", "504", "672"])
    numero_cuenta = st.text_input("NUMERO DE CUENTA")
    tipo = st.selectbox("TIPO", ["Corriente", "Chequera Electronica", "Cuenta RUT", "Ahorro", "VALE VISTA"])
    email = st.text_input("EMAIL")

    guardar_datos = st.form_submit_button("Guardar Datos")

    if guardar_datos:
        # Crear un nuevo DataFrame con los datos ingresados
        data = {
            "RUT": [rut],
            "RUT Completo": [rut + digito],
            "TITULAR": [titular],
            "BANCO": [banco],
            "Cod. Banco": [codigo_banco],
            "NUMERO DE CUENTA": [numero_cuenta],
            "TIPO": [tipo],
            "EMAIL": [email]
        }
        new_df = pd.DataFrame(data)

        # Leer los datos existentes de la hoja de cálculo
        existing_df = conn.read(worksheet=worksheet)

        # Concatenar los datos existentes con los nuevos datos
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Guardar los datos actualizados en la hoja de cálculo
        conn.update(worksheet=worksheet, data=updated_df)

        # Mostrar mensaje de éxito
        st.sidebar.success("Los datos se han guardado correctamente en la hoja de cálculo.")

    # Botón para recargar la página y ver los cambios
if st.sidebar.button("Recargar la página para ver los cambios"):
    st.experimental_rerun()
