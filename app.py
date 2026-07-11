import streamlit as st

# Configuración principal de la página
st.set_page_config(page_title="Portal de BI - ESS", page_icon="🚀", layout="wide")

# Inicializar estados de sesión esenciales
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = "Inicio"

# === INYECCIÓN CSS ULTRA-ESTRICTA Y GLOBAL ===
st.markdown(
    """
    <style>
        /* 1. Fondo principal continuo de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #050530 !important;
        }
        
        /* 2. Estilo base transparente para los botones del menú de módulos */
        [data-testid="stSidebar"] button {
            background-color: transparent !important;
            border: none !important;
            color: #FFFFFF !important;
            width: 100% !important;
            text-align: left !important;
            padding: 12px 15px !important;
            border-radius: 8px !important;
            margin-bottom: 5px !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
        }
        
        /* Forzar que el texto de los botones del menú sea blanco e impecable */
        [data-testid="stSidebar"] button p,
        [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] button div {
            color: #FFFFFF !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
        }

        /* Efecto Hover estilo "Eden" para los módulos */
        [data-testid="stSidebar"] button:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
        }

        /* 3. TÍTULO SECCIÓN: Blanco sutil con opacidad */
        .menu-titulo-custom {
            color: rgba(255, 255, 255, 0.4) !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            margin: 25px 0 10px 15px !important;
            display: block !important;
        }
        
        /* 4. CONTENEDOR FLEX PARA MANDAR EL LOGOUT AL FONDO */
        .sidebar-bottom-container {
            margin-top: auto !important;
            padding-top: 20px !important;
            width: 100% !important;
        }
        
        /* DISEÑO PREMIUM DEL BOTÓN DE CERRAR SESIÓN */
        .btn-logout-box button {
            background-color: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3) !important;
            width: 100% !important;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }

        /* Forzar explícitamente el TEXTO BLANCO en Cerrar Sesión */
        .btn-logout-box button p, 
        .btn-logout-box button span, 
        .btn-logout-box button div {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        /* Hover dinámico: Alerta roja elegante */
        .btn-logout-box button:hover {
            background-color: #D32F2F !important;
            border-color: #D32F2F !important;
        }

        /* 5. Mantener cajas de texto e inputs de Login legibles */
        .stTextInput input {
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
            border: 1px solid #CCCCCC !important;
        }
        .stTextInput label {
            color: #1A1A1A !important;
        }
    </style>
    """,
    unsafe_allow_html=True
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
    st.sidebar.markdown('<span class="menu-titulo-custom">Módulos de Análisis</span>', unsafe_allow_html=True)

    # Diccionario de módulos
    opciones_menu = {
        "Inicio": "🏠 Inicio",
        "Capital Humano": "👥 Capital Humano",
        "Comercial": "💼 Comercial y Ventas",
        "Liquidaciones": "🧮 Liquidaciones",
        "Operaciones": "⚙️ Operaciones",
        "Flotilla": "🚛 Flotilla y Activos",
        "Códigos de Falla": "⚠️ Códigos de Falla"
    }

    # Renderizado y detección de los botones del menú
    for clave, etiqueta in opciones_menu.items():
        if st.session_state.menu_seleccionado == clave:
            etiqueta_final = f"🔹 {etiqueta}"
        else:
            etiqueta_final = etiqueta
            
        if st.sidebar.button(etiqueta_final, key=f"menu_{clave}"):
            st.session_state.menu_seleccionado = clave
            st.rerun()

    # CONTENEDOR DINÁMICO AL FONDO: Coloca y formatea Cerrar Sesión abajo de todo
    with st.sidebar.container():
        st.sidebar.markdown('<div class="sidebar-bottom-container btn-logout-box">', unsafe_allow_html=True)
        if st.sidebar.button("🚪 Cerrar Sesión", key="btn_logout"):
            st.session_state.autenticado = False
            st.session_state.menu_seleccionado = "Inicio"
            st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # === Área Principal de Contenidos ===
    st.title("🚀 Portal de Business Intelligence - ESS")
    st.write("Bienvenido al centro de mando de datos de la organización.")
    st.markdown("---")
    
    area = st.session_state.menu_seleccionado

    if area == "Inicio":
        st.subheader("👋 Selecciona un módulo en la barra de navegación lateral para inicializar los tableros analíticos.")
        st.info("Nota corporativa: Para la descarga o extracción de registros optimizados con métricas DAX, localice las herramientas de exportación dispuestas en la base de cada sección correspondiente.")
        
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
