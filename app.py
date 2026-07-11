import streamlit as st

# Configuración principal de la página
st.set_page_config(page_title="Portal de BI - ESS", page_icon="🚀", layout="wide")

# Inicializar estados de sesión esenciales
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = "Inicio"

# Inyección de estilos CSS Ultra-Estrictos y Globales para la Barra Lateral
st.markdown(
    """
    <style>
        /* 1. Fondo principal continuo de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #050530 !important;
        }
        
        /* 2. Forzar que TODO contenedor de botón dentro de la barra lateral sea transparente */
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
        
        /* 3. Forzar el texto e iconos internos de TODOS los botones en blanco */
        [data-testid="stSidebar"] button p,
        [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] button div {
            color: #FFFFFF !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
        }

        /* 4. Efecto Hover estilo "Eden" (Fondo sutil claro al pasar el cursor) */
        [data-testid="stSidebar"] button:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
        }

        /* 5. TÍTULO SECCIÓN: Blanco semi-transparente elegante */
        .menu-titulo-custom {
            color: rgba(255, 255, 255, 0.4) !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            margin: 25px 0 10px 15px !important;
            display: block !important;
        }
        
        /* 6. BOTÓN EXCLUSIVO CERRAR SESIÓN (Ubicado en la parte superior) */
        .btn-logout-box button {
            background-color: #1E2950 !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important;
        }
        .btn-logout-box button p {
            font-weight: 700 !important;
        }
        .btn-logout-box button:hover {
            background-color: #EF4444 !important; /* Rojo de alerta al hacer hover */
            border-color: #EF4444 !important;
        }

        /* Control de contraste para las cajas del Login */
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

# Vista de Control de Acceso
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
    # Contenedor especial para el botón de Cerrar Sesión superior
    st.sidebar.markdown('<div class="btn-logout-box">', unsafe_allow_html=True)
    if st.sidebar.button("🚪 Cerrar Sesión", key="btn_logout"):
        st.session_state.autenticado = False
        st.session_state.menu_seleccionado = "Inicio"
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Encabezado del Menú en la barra lateral
    st.sidebar.markdown('<span class="menu-titulo-custom">Módulos de Análisis</span>', unsafe_allow_html=True)

    # Diccionario con las opciones limpias y sus respectivos iconos
    opciones_menu = {
        "Inicio": "🏠 Inicio",
        "Capital Humano": "👥 Capital Humano",
        "Comercial": "💼 Comercial y Ventas",
        "Liquidaciones": "🧮 Liquidaciones",
        "Operaciones": "⚙️ Operaciones",
        "Flotilla": "🚛 Flotilla y Activos",
        "Códigos de Falla": "⚠️ Códigos de Falla"
    }

    # Renderizado y detección del estado activo del menú
    for clave, etiqueta in opciones_menu.items():
        # Si está seleccionado, le agregamos un indicador visual y estilo limpio
        if st.session_state.menu_seleccionado == clave:
            etiqueta_final = f"🔹 {etiqueta}"
        else:
            etiqueta_final = etiqueta
            
        if st.sidebar.button(etiqueta_final, key=f"menu_{clave}"):
            st.session_state.menu_seleccionado = clave
            st.rerun()

    # --- Área Principal de Contenidos ---
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
