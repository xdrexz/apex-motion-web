import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(
    page_title="Apex Motion - Diseño & Desarrollo Web",
    page_icon="⚡",
    layout="wide"
)

# 2. Estilos personalizados
st.markdown("""
    <style>
    .stApp {
        background-color: #001219;
        color: #ffffff;
    }
    div[data-testid="stVerticalBlock"] > div {
        background-color: #14213d;
        border-radius: 12px;
        padding: 20px;
    }
    .stButton > button, div.stLinkButton > a {
        background-color: #0a9396 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100%;
    }
    .stButton > button:hover, div.stLinkButton > a:hover {
        background-color: #087072 !important;
        color: #ffffff !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado
st.title("⚡ Apex Motion")
st.subheader("Transformamos tu negocio con páginas web de alto impacto")

col1, col2 = st.columns(2)
with col1:
    st.info("⏱️ **Tiempo de entrega:** 3 a 7 días hábiles")
with col2:
    st.info("🕒 **Horario de atención:** Lunes a Viernes de 7:00 a 20:00")

st.divider()

# 4. Planes
st.header("Servicios & Planes")

PLANES = {
    "Web Emprendedor - Q1,200": {
        "precio": "Q1,200", 
        "desc": "Landing Page de 1 sola página, diseño responsivo, botón a WhatsApp"
    },
    "Web Profesional - Q2,500": {
        "precio": "Q2,500", 
        "desc": "Sitio completo hasta 5 secciones, optimización SEO básica, redes sociales"
    },
    "Tienda Online - Q4,000": {
        "precio": "Q4,000", 
        "desc": "Catálogo de productos, pasarela de pagos, panel de administración"
    }
}

plan_seleccionado = st.radio("Selecciona tu plan ideal:", list(PLANES.keys()))
detalles = PLANES[plan_seleccionado]

st.write(f"**Detalles del plan:** {detalles['desc']}")

# 5. Enlace a WhatsApp
telefono = "50259839777"
mensaje = f"Hola Apex Motion, me interesa solicitar información sobre el plan: {plan_seleccionado}"
url_whatsapp = f"https://wa.me/{telefono}?text={urllib.parse.quote(mensaje)}"

st.divider()
st.link_button("📲 Solicitar este Plan por WhatsApp", url_whatsapp)
