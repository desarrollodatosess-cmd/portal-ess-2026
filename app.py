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
            padding-top: 25px !important;
        }
        
        /* === TÍTULO DEL MENÚ EN BLANCO SEMI-TRANSPARENTE === */
        .menu-titulo {
            color: rgba(255, 255, 255, 0.6) !important; /* Blanco al 60% de opacidad */
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin: 25px 0 12px 12px !important;
        }
        
        /* Estilo base para los botones de navegación simulados */
        div.stButton > button {
            width: 100% !important;
            background-color: transparent !important;
            color: rgba(255, 255, 255, 0.8) !important;
            border: none !important;
            padding: 10px 15px !important;
            text-align: left !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            margin-bottom: 5px !important;
            transition: all 0.2s ease-in-out !important;
            display: flex !important;
            align-items: center !important;
        }
        
        /* Efecto Hover: Al pasar el cursor sobre una opción del menú */
        div.stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #FFFFFF !important;
        }
        
        /* === BOTÓN DE CERRAR SESIÓN ALTAMENTE NOTABLE Y LIMPIO === */
        .boton-cerrar div.stButton > button {
            background-color: #1E2950 !important; /* Fondo azul sólido más claro para resaltar */
            color: #FFFFFF !important;            /* Texto blanco brillante */
            border: 1px solid rgba(255, 255, 255, 0.2) !important; /* Borde fino elegante */
            font-weight: 700 !important;          /* Letra gruesa notable */
            font-size: 0.95rem !important;
            border-radius: 8px !important;
            margin-bottom: 20px !important;
            text-align: center !important;
            justify-content: center !important;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important; /* Sombra sutil de elevación */
        }
        
        /* Hover del botón Cerrar Sesión: Alerta en Rojo */
        .boton-cerrar div.stButton > button:hover {
            background-color: #EF4444 !important; /* Cambia a rojo intenso */
            color: #FFFFFF !important;
            border-color: #EF4444 !important;
            box-shadow: 0px 4px 12px rgba(239, 68, 68, 0.3) !important;
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
    # 1. Componente Superior: Cerrar Sesión estilizado y visible
    st.sidebar.markdown('<div class="boton-cerrar">', unsafe_allow_html=True)
    if st.sidebar.button("🚪 Cerrar Sesión", key="btn_logout"):
        st.session_state.autenticado = False
        st.session_state.menu_seleccionado = "Inicio"
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Título organizador del menú con el color blanco transparente aplicado
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
        # Añadir indicador visual al elemento seleccionado de forma integrada
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
