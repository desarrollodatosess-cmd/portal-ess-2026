import streamlit as st

# Configuración principal de la página
st.set_page_config(page_title="Portal de BI - ESS", page_icon="🚀", layout="wide")

# Inicializar estados de sesión esenciales
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = "Inicio"

# Inyección de estilos CSS Ultra-Estrictos para corregir el contraste del texto
st.markdown(
    """
    <style>
        /* Fondo principal de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #050530 !important;
        }
        
        /* === TÍTULO MÓDULOS DE ANÁLISIS: BLANCO TRANSPARENTOSO SOFISTICADO === */
        .menu-titulo-custom {
            color: rgba(255, 255, 255, 0.55) !important; /* Blanco al 55% de opacidad */
            font-size: 0.82rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            margin: 20px 0px 15px 12px !important;
            display: block !important;
        }
        
        /* === BOTÓN DE CERRAR SESIÓN: DISEÑO SÓLIDO Y DESTACADO === */
        #contenedor-logout div.stButton > button {
            background-color: #1E2950 !important; /* Fondo azul más claro */
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            width: 100% !important;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            text-align: center !important;
            justify-content: center !important;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.2s ease-in-out !important;
        }
        
        /* Forzar texto blanco en Cerrar Sesión */
        #contenedor-logout div.stButton > button p,
        #contenedor-logout div.stButton > button span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }
        
        /* Hover del botón Cerrar Sesión (Cambio a Alerta) */
        #contenedor-logout div.stButton > button:hover {
            background-color: #EF4444 !important;
            border-color: #EF4444 !important;
        }

        /* === BOTONES DEL MENÚ DE ÁREAS: TEXTO BLANCO LIMPIO Y VISIBLE === */
        #contenedor-menu div.stButton > button {
            width: 100% !important;
            background-color: transparent !important;
            border: none !important;
            padding: 10px 12px !important;
            text-align: left !important;
            border-radius: 6px !important;
            margin-bottom: 4px !important;
            display: flex !important;
            align-items: center !important;
            transition: all 0.2s ease !important;
        }
        
        /* FORZAR COLOR BLANCO EN EL TEXTO DE LOS BOTONES NATIVOS */
        #contenedor-menu div.stButton > button p,
        #contenedor-menu div.stButton > button span {
            color: rgba(255, 255, 255, 0.9) !important; /* Blanco brillante de alta visibilidad */
            font-size: 0.98rem !important;
            font-weight: 500 !important;
        }
        
        /* Efecto Hover elegante para las opciones */
        #contenedor-menu div.stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.08) !important;
        }
        #contenedor-menu div.stButton > button:hover p,
        #contenedor-menu div.stButton > button:hover span {
            color: #FFFFFF !important;
        }

        /* Mantener las cajas de Login legibles */
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
    # Botón superior de Cerrar Sesión
    st.sidebar.markdown('<div id="contenedor-logout">', unsafe_allow_html=True)
    if st.sidebar.button("🚪 Cerrar Sesión", key="btn_logout"):
        st.session_state.autenticado = False
        st.session_state.menu_seleccionado = "Inicio"
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Título del menú con la opacidad corregida
    st.sidebar.markdown('<span class="menu-titulo-custom">Módulos de Análisis</span>', unsafe_allow_html=True)

    # Bloque de navegación principal
    st.sidebar.markdown('<div id="contenedor-menu">', unsafe_allow_html=True)
    
    opciones_menu = {
        "Inicio": "🏠 Inicio",
        "Capital Humano": "👥 Capital Humano",
        "Comercial": "💼 Comercial y Ventas",
        "Liquidaciones": "🧮 Liquidaciones",
        "Operaciones": "⚙️ Operaciones",
        "Flotilla": "🚛 Flotilla y Activos",
        "Códigos de Falla": "⚠️ Códigos de Falla"
    }

    for clave, etiqueta in opciones_menu.items():
        if st.session_state.menu_seleccionado == clave:
            etiqueta_final = f"🔹 {etiqueta}"
        else:
            etiqueta_final = etiqueta
            
        if st.sidebar.button(etiqueta_final, key=f"menu_{clave}"):
            st.session_state.menu_seleccionado = clave
            st.rerun()
            
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # 3. Despliegue de Contenidos Dinámicos en el Área Principal
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
