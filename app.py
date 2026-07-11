import streamlit as st

# Configuración principal de la página
st.set_page_config(page_title="Portal de BI - ESS", page_icon="🚀", layout="wide")

# Inicializar el estado de la sesión para el login si no existe
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Función para verificar credenciales
def verificar_login(usuario, contrasena):
    # Aquí puedes cambiar el usuario y contraseña por los que tú quieras
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
    # Botón para cerrar sesión en la esquina superior
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🚀 Portal de Business Intelligence - ESS")
    st.write("Bienvenido al centro de mando de datos.")
    
    # Menú lateral para las áreas de la empresa
    area = st.sidebar.selectbox(
        "Selecciona el área que deseas consultar:",
        ["Inicio", "Ventas", "Finanzas", "Operaciones"]
    )
    
    if area == "Inicio":
        st.subheader("👋 Selecciona un área en el menú de la izquierda para ver los tableros.")
        
    elif area == "Ventas":
        st.subheader("📊 Tablero del Área de Ventas")
        st.write("Aquí colocaremos el reporte de Power BI de Ventas en el siguiente paso.")
        
    elif area == "Finanzas":
        st.subheader("💰 Tablero del Área de Finanzas")
        st.write("Aquí colocaremos el reporte de Power BI de Finanzas en el siguiente paso.")
        
    elif area == "Operaciones":
        st.subheader("⚙️ Tablero del Área de Operaciones")
        st.write("Aquí colocaremos el reporte de Power BI de Operaciones en el siguiente paso.")
