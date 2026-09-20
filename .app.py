"""
Apex Motion — Diseño y desarrollo web
--------------------------------------
Aplicación Streamlit de una sola página para presentar los planes de
servicio de Apex Motion y generar una cotización lista para enviar por
WhatsApp con un solo clic.

Ejecutar con:
    streamlit run app.py
"""

import urllib.parse

import streamlit as st

# =============================================================================
# CAMBIA AQUÍ TUS DATOS DE CONTACTO Y SERVICIO
# =============================================================================
COMPANY_NAME = "Apex Motion"
COMPANY_TAGLINE = "Diseñamos y construimos el sitio web que tu negocio necesita para vender más."

WHATSAPP_NUMBER = "50259839777"  # Formato internacional, solo dígitos, sin "+"

DELIVERY_TIME = "3 a 7 días hábiles"
BUSINESS_HOURS = "Lunes a Viernes de 7:00 a 20:00"

CURRENCY = "Q"  # Símbolo de moneda usado en toda la página (Quetzales)

# --- PLANES / PRECIOS -------------------------------------------------------
# id:        identificador único (sin espacios) usado internamente
# name:      nombre visible del plan
# tagline:   una línea corta describiendo para quién es el plan
# price:     precio del plan en números (sin símbolo de moneda)
# featured:  True para destacar el plan como "Más elegido"
# features:  lista de características que se muestran como checklist
PLANS = [
    {
        "id": "emprendedor",
        "name": "Web Emprendedor",
        "tagline": "Ideal para empezar con una presencia online simple y directa.",
        "price": 1200,
        "featured": False,
        "features": [
            "Landing page de una sola página",
            "Diseño responsivo (móvil, tablet, escritorio)",
            "Botón directo a WhatsApp",
        ],
    },
    {
        "id": "profesional",
        "name": "Web Profesional",
        "tagline": "El plan más elegido: un sitio completo para tu negocio.",
        "price": 1500,
        "featured": True,
        "features": [
            "Sitio completo de hasta 5 secciones",
            "Optimización SEO básica",
            "Integración con redes sociales",
        ],
    },
    {
        "id": "ecommerce",
        "name": "Tienda Online / E-commerce",
        "tagline": "Para vender tus productos directamente desde tu sitio.",
        "price": 3000,
        "featured": False,
        "features": [
            "Catálogo de productos",
            "Pasarela de pagos integrada",
            "Panel de administración",
        ],
    },
]

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title=f"{COMPANY_NAME} — Diseño y desarrollo web",
    page_icon="🚀",
    layout="wide",
)

# =============================================================================
# ESTILOS (paleta oficial de Apex Motion)
# =============================================================================
st.markdown(
    """
    <style>
    :root{
        --primary-color:   #000000;   /* Fondo principal / texto */
        --bg-color:        #001219;   /* Fondo general de la página */
        --secondary-color: #14213d;   /* Tarjetas y contenedores */
        --accent-color:    #0a9396;   /* Botones y destacados */
        --accent-color-dark: #07686a;
        --text-strong: #ffffff;
        --text-soft:   #e5e5e5;
    }

    /* Fondo general de la app */
    .stApp{
        background-color: var(--bg-color);
        color: var(--text-strong);
    }

    /* Asegurar texto legible en blanco/gris claro sobre fondo oscuro */
    h1, h2, h3, h4, h5, h6, p, span, label, li, div{
        color: var(--text-strong);
    }
    .subtle-text{ color: var(--text-soft) !important; }

    /* Header */
    .am-header{
        text-align: center;
        padding: 2.2rem 1rem 1.4rem 1rem;
    }
    .am-header h1{
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        letter-spacing: -0.01em;
    }
    .am-header h1 span{ color: var(--accent-color); }
    .am-header p{
        font-size: 1.15rem;
        color: var(--text-soft) !important;
        max-width: 640px;
        margin: 0 auto;
    }

    /* Tarjetas informativas (entrega / horario) */
    .info-card{
        background-color: var(--secondary-color);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        text-align: center;
        height: 100%;
    }
    .info-card .info-label{
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: .06em;
        color: var(--accent-color) !important;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .info-card .info-value{
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text-strong) !important;
    }

    /* Tarjetas de planes */
    .plan-card{
        background-color: var(--secondary-color);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 1.6rem 1.4rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
    }
    .plan-card.featured{
        border: 1.5px solid var(--accent-color);
        box-shadow: 0 0 0 3px rgba(10,147,150,0.18);
    }
    .plan-badge{
        display: inline-block;
        background-color: var(--accent-color);
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        margin-bottom: 0.7rem;
        width: fit-content;
    }
    .plan-name{
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: var(--text-strong) !important;
    }
    .plan-tagline{
        font-size: 0.92rem;
        color: var(--text-soft) !important;
        min-height: 42px;
        margin-bottom: 0.8rem;
    }
    .plan-price{
        font-size: 2.1rem;
        font-weight: 800;
        color: var(--accent-color) !important;
        margin-bottom: 0.9rem;
    }
    .plan-price span{
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--text-soft) !important;
    }
    .plan-features{
        list-style: none;
        padding-left: 0;
        margin-bottom: 0.5rem;
        flex-grow: 1;
    }
    .plan-features li{
        font-size: 0.92rem;
        color: var(--text-soft) !important;
        padding: 0.3rem 0;
        padding-left: 1.4rem;
        position: relative;
    }
    .plan-features li::before{
        content: "✓";
        position: absolute;
        left: 0;
        color: var(--accent-color);
        font-weight: 700;
    }

    /* Radio buttons de selección de plan: los agrandamos un poco */
    div[role="radiogroup"] label{
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* Botones generales de Streamlit */
    .stButton > button{
        background-color: var(--accent-color);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        font-weight: 700;
        width: 100%;
        transition: background-color .15s ease, transform .15s ease;
    }
    .stButton > button:hover{
        background-color: var(--accent-color-dark);
        color: #ffffff;
        transform: translateY(-1px);
    }

    /* Botón de enlace (WhatsApp) */
    .stLinkButton > a{
        background-color: var(--accent-color) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100%;
        text-align: center;
        transition: background-color .15s ease, transform .15s ease;
    }
    .stLinkButton > a:hover{
        background-color: var(--accent-color-dark) !important;
        transform: translateY(-1px);
    }

    /* Resumen de cotización */
    .quote-box{
        background-color: var(--primary-color);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        padding: 1.6rem;
        margin-top: 1rem;
    }
    .quote-box h3{
        color: var(--text-strong) !important;
        margin-bottom: 0.6rem;
    }
    .quote-total{
        font-size: 2rem;
        font-weight: 800;
        color: var(--accent-color) !important;
        margin: 0.6rem 0 1rem 0;
    }

    /* Inputs de texto */
    .stTextInput input, .stTextArea textarea{
        background-color: var(--secondary-color) !important;
        color: var(--text-strong) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 8px !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder{
        color: rgba(229,229,229,0.55) !important;
    }
    label{ color: var(--text-soft) !important; }

    hr{ border-color: rgba(255,255,255,0.12) !important; }

    footer, #MainMenu{ visibility: hidden; }
    .am-footer{
        text-align: center;
        color: rgba(229,229,229,0.55) !important;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# ENCABEZADO
# =============================================================================
st.markdown(
    f"""
    <div class="am-header">
        <h1><span>{COMPANY_NAME}</span></h1>
        <p>{COMPANY_TAGLINE}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# INFORMACIÓN DE SERVICIO Y GARANTÍA
# =============================================================================
info_col1, info_col2 = st.columns(2)
with info_col1:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">Tiempo de entrega</div>
            <div class="info-value">{DELIVERY_TIME}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with info_col2:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">Horario de atención</div>
            <div class="info-value">{BUSINESS_HOURS}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# SECCIÓN DE PLANES
# =============================================================================
st.markdown("## Nuestros planes")
st.markdown(
    '<p class="subtle-text">Elige el plan que mejor se adapte a tu negocio. '
    'El precio mostrado es el total del proyecto, sin costos adicionales.</p>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

plan_cols = st.columns(3)
for col, plan in zip(plan_cols, PLANS):
    with col:
        featured_class = "plan-card featured" if plan["featured"] else "plan-card"
        badge_html = '<div class="plan-badge">Más elegido</div>' if plan["featured"] else ""
        features_html = "".join(f"<li>{feature}</li>" for feature in plan["features"])

        st.markdown(
            f"""
            <div class="{featured_class}">
                {badge_html}
                <div class="plan-name">{plan['name']}</div>
                <div class="plan-tagline">{plan['tagline']}</div>
                <div class="plan-price">{CURRENCY}{plan['price']:,}<span> / proyecto</span></div>
                <ul class="plan-features">{features_html}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# SELECCIÓN DE PLAN
# =============================================================================
st.markdown("## Elige tu plan")

plan_labels = [f"{plan['name']} — {CURRENCY}{plan['price']:,}" for plan in PLANS]
selected_label = st.radio(
    "Selecciona el plan que quieres cotizar:",
    options=plan_labels,
    index=1,  # Web Profesional preseleccionado por ser el más elegido
)
selected_plan = PLANS[plan_labels.index(selected_label)]

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# DATOS DE CONTACTO DEL CLIENTE (opcional, se incluyen en el mensaje)
# =============================================================================
st.markdown("## Tus datos")
st.markdown(
    '<p class="subtle-text">Estos datos son opcionales, pero nos ayudan a atenderte más rápido.</p>',
    unsafe_allow_html=True,
)

contact_col1, contact_col2 = st.columns(2)
with contact_col1:
    client_name = st.text_input("Nombre", placeholder="Tu nombre")
with contact_col2:
    client_business = st.text_input("Nombre de tu negocio (opcional)", placeholder="Ej. Panadería Don José")

client_notes = st.text_area(
    "¿Algo más que debamos saber? (opcional)",
    placeholder="Ej. Necesito el sitio en español e inglés...",
)

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# RESUMEN Y COTIZACIÓN
# =============================================================================
st.markdown("## Resumen de tu cotización")

st.markdown(
    f"""
    <div class="quote-box">
        <h3>{selected_plan['name']}</h3>
        <p class="subtle-text">{selected_plan['tagline']}</p>
        <div class="quote-total">{CURRENCY}{selected_plan['price']:,}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


def build_whatsapp_message(plan: dict, name: str, business: str, notes: str) -> str:
    """Arma el mensaje de cotización que se enviará por WhatsApp."""
    greeting_name = name.strip() if name.strip() else "un cliente interesado"
    lines = [
        f"Hola {COMPANY_NAME}, soy {greeting_name}.",
        "",
        "Quiero solicitar una cotización con el siguiente plan:",
        f"• Plan: {plan['name']}",
        f"• Precio: {CURRENCY}{plan['price']:,}",
        f"• Tiempo de entrega estimado: {DELIVERY_TIME}",
    ]

    if business.strip():
        lines.insert(1, f"Mi negocio se llama: {business.strip()}")

    if notes.strip():
        lines.append("")
        lines.append(f"Notas adicionales: {notes.strip()}")

    lines.append("")
    lines.append("¿Podrían confirmarme disponibilidad para iniciar el proyecto?")

    return "\n".join(lines)


whatsapp_message = build_whatsapp_message(selected_plan, client_name, client_business, client_notes)
whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(whatsapp_message)}"

with st.expander("Ver mensaje que se enviará por WhatsApp"):
    st.text(whatsapp_message)

st.link_button(
    f"📲 Solicitar cotización de {selected_plan['name']} por WhatsApp",
    whatsapp_url,
    use_container_width=True,
)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown(
    f"""
    <div class="am-footer">
        © 2026 {COMPANY_NAME}. Todos los derechos reservados. · WhatsApp: +{WHATSAPP_NUMBER}
    </div>
    """,
    unsafe_allow_html=True,
)
