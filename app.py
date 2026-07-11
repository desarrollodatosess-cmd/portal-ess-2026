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
        
        /* 2. Reducir el espacio general del contenedor interno de Streamlit */
        [data-testid="stSidebarContent"] {
            display: flex !important;
            flex-direction: column !important;
            height: 100vh !important;
            justify-content: flex-start !important;
            padding-bottom: 80px !important; /* Espacio para que no tape el botón del fondo */
        }
        
        /* 3. Estilo base transparente y MENOS DISTANCIA para los botones de módulos */
        [data-testid="stSidebar"] button {
            background-color: transparent !important;
            border: none !important;
            color: #FFFFFF !important;
            width: 100% !important;
            text-align: left !important;
            padding: 6px 12px !important; /* Reducido de 12px a 6px para menor distancia */
            border-radius: 8px !important;
            margin-bottom: 2px !important; /* Distancia mínima entre botones */
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
        }
        
        /* Forzar texto blanco en botones normales */
        [data-testid="stSidebar"] button p,
        [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] button div {
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
        }

        /* Hover estilo "Eden" para los módulos */
        [data-testid="stSidebar"] button:hover {
            background-color: rgba(255, 255, 255, 0.08) !important;
        }

        /* TÍTULO SECCIÓN */
        .menu-titulo-custom {
            color: rgba(255, 255, 255, 0.4) !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            margin: 15px 0 8px 12px !important;
            display: block !important;
        }
        
        /* 4. POSICIONAMIENTO DEL BOTÓN AL PIE DE LA BARRA LATERAL */
        .sidebar-bottom-container {
            position: absolute !important;
            bottom: 20px !important;
            left: 0 !important;
            width: 100% !important;
            padding: 0 16px !important;
            box-sizing: border-box !important;
            background-color: #050530 !important;
            z-index: 999 !important;
        }
        
        /* DISEÑO FIJO DEL BOTÓN DE CERRAR SESIÓN (Caja premium de image_303a9b) */
        .sidebar-bottom-container button {
            background-color: rgba(255, 255, 255, 0.12) !important; /* Fondo gris/azul sutil */
            border: 1px solid rgba(255, 255, 255, 0.2) !important; /* Borde visible */
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3) !important;
            width: 100% !important;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
        }

        /* TEXTO BLANCO EXCLUSIVO para Cerrar Sesión */
        .sidebar-bottom-container button p, 
        .sidebar-bottom-container button span, 
        .sidebar-bottom-container button div {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        /* Hover dinámico para Cerrar Sesión */
        .sidebar-bottom-container button:hover {
            background-color: #D32F2F !important;
            border-color: #D32F2F !important;
        }

        /* Mantener cajas de Login legibles */
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

    # Renderizado de los botones del menú (con menor distancia por CSS)
    for clave, etiqueta in opciones_menu.items():
        if st.session_state.menu_seleccionado == clave:
            etiqueta_final = f"🔹 {etiqueta}"
        else:
            etiqueta_final = etiqueta
            
        if st.sidebar.button(etiqueta_final, key=f"menu_{clave}"):
            st.session_state.menu_seleccionado = clave
            st.rerun()

    # EL BOTÓN DE CERRAR SESIÓN SE ANCLA AL PIE DE LA BARRA LATERAL
    st.sidebar.markdown('<div class="sidebar-bottom-container">', unsafe_allow_html=True)
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
