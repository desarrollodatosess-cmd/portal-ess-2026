import streamlit as st

# Configuración principal de la página
st.set_page_config(page_title="Portal de BI - ESS", page_icon="🚀", layout="wide")

# Forzar diseño visual (Cajas blancas, texto visible y barra lateral azul marino)
st.markdown(
    """
    <style>
        /* Fondo de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #050530 !important;
        }
        /* Texto dentro de la barra lateral */
        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
            color: #FFFFFF !important;
        }
        /* Estilo para las cajas de entrada de texto (Login) */
        .stTextInput input {
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
            border: 1px solid #CCCCCC !important;
        }
        /* Títulos de las cajas de login */
        .stTextInput label {
            color: #1A1A1A !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar el estado de la sesión para el login si no existe
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Función para verificar credenciales
def verificar_login(usuario, contrasena):
    if usuario == "admin" and contrasena == "ess2026":
        st.session_state.autenticado = True
        st.success("¡Acceso concedido!")
        st.rerun()
    else:
        st.error("Usuario o contraseña incorrectos")

# Si el usuario NO está autenticado, mostramos la pantalla de Login
if not st.session_state.autenticado:
    st.title("🔒 Control de Acceso - Portal ESS")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        usuario_ingresado = st.text_input("Usuario")
        contrasena_ingresada = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            verificar_login(usuario_ingresado, contrasena_ingresada)

# Si el usuario SÍ está autenticado, entra al portal
else:
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🚀 Portal de Business Intelligence - ESS")
    st.write("Bienvenido al centro de mando de datos de la organización.")
    st.markdown("---")
    
    # Menú lateral con tus 6 áreas reales
    area = st.sidebar.selectbox(
        "Selecciona el área que deseas consultar:",
        [
            "Inicio", 
            "Capital Humano", 
            "Comercial", 
            "Liquidaciones", 
            "Operaciones", 
            "Flotilla", 
            "Códigos de Falla"
        ]
    )
    
    if area == "Inicio":
        st.subheader("👋 Selecciona un área en el menú de la izquierda para desplegar los tableros analíticos.")
        st.info("Nota: Para descargar datos específicos con lógica DAX, ubica el botón de descarga debajo del tablero correspondiente en cada sección.")
        
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
