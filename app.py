import re
import streamlit as st

# Configuración principal de la página
st.set_page_config(page_title="Portal de BI - ESS", page_icon="🚀", layout="wide")

# Inicializar estados de sesión esenciales
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = "Inicio"


def slugify(texto: str) -> str:
    """Convierte 'Capital Humano' -> 'capital_humano' para usarlo como key/clase CSS."""
    texto = texto.lower()
    for a, b in {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}.items():
        texto = texto.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", texto).strip("_")


# === INYECCIÓN CSS ULTRA-ESTRICTA Y GLOBAL ===
slug_seleccionado = slugify(st.session_state.menu_seleccionado)

st.markdown(
    f"""
    <style>
        /* 1. Fondo principal continuo de la barra lateral */
        [data-testid="stSidebar"] {{
            background-color: #0E0E3A !important;
        }}

        /* 2. Layout general: menú arriba, logout pegado abajo */
        [data-testid="stSidebarContent"] {{
            display: flex !important;
            flex-direction: column !important;
            height: 100vh !important;
            padding-top: 10px !important;
            padding-bottom: 20px !important;
        }}

        /* TÍTULO SECCIÓN */
        .menu-titulo-custom {{
            color: rgba(255, 255, 255, 0.35) !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            margin: 10px 0 10px 14px !important;
            display: block !important;
        }}

        /* 3. Estilo base de TODOS los botones del menú (estado inactivo) */
        [data-testid="stSidebar"] [data-testid="stButton"] button {{
            background-color: transparent !important;
            border: none !important;
            color: #B7B9D6 !important;
            width: 100% !important;
            text-align: left !important;
            padding: 10px 14px !important;
            border-radius: 10px !important;
            margin-bottom: 2px !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 10px !important;
            transition: background-color 0.2s ease, color 0.2s ease !important;
        }}

        [data-testid="stSidebar"] [data-testid="stButton"] button p,
        [data-testid="stSidebar"] [data-testid="stButton"] button span,
        [data-testid="stSidebar"] [data-testid="stButton"] button div {{
            color: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
        }}

        /* Hover estilo para los módulos */
        [data-testid="stSidebar"] [data-testid="stButton"] button:hover {{
            background-color: rgba(255, 255, 255, 0.07) !important;
            color: #FFFFFF !important;
        }}

        /* 4. BOTÓN ACTIVO: se pinta solo el contenedor cuya key coincide con la selección */
        .st-key-menu_{slug_seleccionado} button {{
            background-color: #4B4FE8 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            box-shadow: 0px 4px 10px rgba(75, 79, 232, 0.35) !important;
        }}

        /* Separador antes de Cerrar Sesión */
        .sidebar-divider {{
            border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
            margin: 8px 14px 10px 14px !important;
        }}

        /* Empuja el bloque de logout al fondo de la barra lateral */
        .sidebar-bottom-container {{
            margin-top: auto !important;
        }}

        .sidebar-bottom-container [data-testid="stButton"] button:hover {{
            background-color: rgba(211, 47, 47, 0.18) !important;
            color: #FF6B6B !important;
        }}

        /* Mantener cajas de Login legibles */
        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
            border: 1px solid #CCCCCC !important;
        }}
        .stTextInput label {{
            color: #1A1A1A !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Lógica de Validación de Login
def verificar_login(usuario, contrasena):
    if usuario == "admin" and contrasena == "ess2026":
        st.session_state.autenticado = True
        st.success("¡Acceso concedido!")
        st.rerun()
    else:
        st.error("Usuario o contraseña incorrectos")


# Vista de Control de Acceso (Login)
if not st.session_state.autenticado:
    st.title("🔒 Control de Acceso - Portal ESS")
    col1, col2 = st.columns([1, 2])
    with col1:
        usuario_ingresado = st.text_input("Usuario")
        contrasena_ingresada = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            verificar_login(usuario_ingresado, contrasena_ingresada)

# Vista Principal del Portal (Autenticado)
else:
    # Encabezado del Menú en la barra lateral
    st.sidebar.markdown(
        '<span class="menu-titulo-custom">Módulos de Análisis</span>',
        unsafe_allow_html=True,
    )

    # Diccionario de módulos: clave -> (icono, etiqueta)
    opciones_menu = {
        "Inicio": ("🏠", "Inicio"),
        "Capital Humano": ("👥", "Capital Humano"),
        "Comercial": ("💼", "Comercial y Ventas"),
        "Liquidaciones": ("🧮", "Liquidaciones"),
        "Operaciones": ("⚙️", "Operaciones"),
        "Flotilla": ("🚛", "Flotilla y Activos"),
        "Códigos de Falla": ("⚠️", "Códigos de Falla"),
    }

    # Renderizado de los botones del menú.
    # Cada botón va dentro de un st.container(key=...) para poder
    # apuntarle con CSS individualmente (clase .st-key-<key>).
    for clave, (icono, etiqueta) in opciones_menu.items():
        slug = slugify(clave)
        with st.sidebar.container(key=f"menu_{slug}"):
            if st.button(f"{icono}  {etiqueta}", key=f"btn_{slug}"):
                st.session_state.menu_seleccionado = clave
                st.rerun()

    # Separador + botón de Cerrar Sesión anclado al pie de la barra lateral
    with st.sidebar:
        st.markdown('<div class="sidebar-bottom-container">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        if st.button("🚪  Cerrar Sesión", key="btn_logout"):
            st.session_state.autenticado = False
            st.session_state.menu_seleccionado = "Inicio"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # === Área Principal de Contenidos ===
    st.title("🚀 Portal de Business Intelligence - ESS")
    st.write("Bienvenido al centro de mando de datos de la organización.")
    st.markdown("---")

    area = st.session_state.menu_seleccionado

    if area == "Inicio":
        st.subheader(
            "👋 Selecciona un módulo en la barra de navegación lateral para "
            "inicializar los tableros analíticos."
        )
        st.info(
            "Nota corporativa: Para la descarga o extracción de registros "
            "optimizados con métricas DAX, localice las herramientas de "
            "exportación dispuestas en la base de cada sección correspondiente."
        )

    elif area == "Capital Humano":
        st.subheader("👥 Indicadores de Capital Humano")
        st.write("Aquí se incrustará el tablero de Capital Humano.")

    elif area == "Comercial":
        st.subheader("💼 Tablero Comercial y Ventas")
        st.write("Aquí se incrustará el tablero Comercial.")

    elif area == "Liquidaciones":
        st.subheader("🧮 Módulo de Liquidaciones")
        st.write("Aquí se incrustará el tablero de Liquidaciones.")

    elif area == "Operaciones":
        st.subheader("⚙️ Control de Operaciones")
        st.write("Aquí se incrustará el tablero de Operaciones.")

    elif area == "Flotilla":
        st.subheader("🚛 Gestión de Flotilla y Activos")
        st.write("Aquí se incrustará el tablero de Flotilla.")

    elif area == "Códigos de Falla":
        st.subheader("⚠️ Análisis de Códigos de Falla")
        st.write("Aquí se incrustará el tablero de Códigos de Falla.")
