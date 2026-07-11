import streamlit as st

# Configuración principal de la página
st.set_page_config(page_title="Portal de BI - ESS", page_icon="🚀", layout="wide")

# Inicializar estados de sesión esenciales
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = "Inicio"

# Inyección de estilos CSS Avanzados para emular un menú UI/UX Premium
st.markdown(
    """
    <style>
        /* Fondo e identidad visual de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #050530 !important;
            padding-top: 20px !important;
        }
        
        /* Contenedor del título del menú */
        .menu-titulo {
            color: #FFFFFF;
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 20px 0 10px 10px;
            opacity: 0.7;
        }
        
        /* Estilo base para los botones de navegación simulados */
        div.stButton > button {
            width: 100% !important;
            background-color: transparent !important;
            color: rgba(255, 255, 255, 0.75) !important;
            border: none !important;
            padding: 10px 15px !important;
            text-align: left !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            margin-bottom: 4px !important;
            transition: all 0.2s ease-in-out !important;
            display: flex !important;
            align-items: center !important;
        }
        
        /* Efecto Hover: Al pasar el cursor sobre una opción */
        div.stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #FFFFFF !important;
        }
        
        /* Estilo específico para resaltar el botón de Cerrar Sesión de forma sobria */
        .boton-cerrar div.stButton > button {
            background-color: rgba(239, 68, 68, 0.15) !important;
            color: #F87171 !important;
            border: 1px solid rgba(239, 68, 68, 0.2) !important;
            font-weight: 600 !important;
            margin-bottom: 30px !important;
            text-align: center !important;
            justify-content: center !important;
        }
        .boton-cerrar div.stButton > button:hover {
            background-color: #EF4444 !important;
            color: #FFFFFF !important;
            border-color: #EF4444 !important;
        }

        /* Restaurar cajas del Login para que mantengan contraste nítido */
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
    # 1. Componente Superior: Cerrar Sesión estilizado
    st.sidebar.markdown('<div class="boton-cerrar">', unsafe_allow_html=True)
    if st.sidebar.button("🚪 Cerrar Sesión", key="btn_logout"):
        st.session_state.autenticado = False
        st.session_state.menu_seleccionado = "Inicio"
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Título organizador del menú lateral
    st.sidebar.markdown('<p class="menu-titulo">Módulos de Análisis</p>', unsafe_allow_html=True)

    # 2. Configuración del Menú de Navegación Vertical con Iconos Limpios
    opciones_menu = {
        "Inicio": "🏠 Inicio",
        "Capital Humano": "👥 Capital Humano",
        "Comercial": "💼 Comercial y Ventas",
        "Liquidaciones": "🧮 Liquidaciones",
        "Operaciones": "⚙️ Operaciones",
        "Flotilla": "🚛 Flotilla y Activos",
        "Códigos de Falla": "⚠️ Códigos de Falla"
    }

    # Renderizar cada opción como un botón de bloque UI elegante
    for clave, etiqueta in opciones_menu.items():
        # Añadir un indicador visual sutil al botón activo
        if st.session_state.menu_seleccionado == clave:
            etiqueta_final = f"🔹 {etiqueta}"
        else:
            etiqueta_final = etiqueta
            
        if st.sidebar.button(etiqueta_final, key=f"menu_{clave}"):
            st.session_state.menu_seleccionado = clave
            st.rerun()

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
