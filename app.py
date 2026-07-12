import base64
import io  # Para crear el Excel en memoria
import re
from pathlib import Path

import numpy as np  # Para manejar la lógica de división entre cero de Pandas
import pandas as pd  # Para procesar los datos
import pyodbc  # <-- INTEGRADO: Conexión nativa SQL Server para Pandas
import streamlit as st
import streamlit.components.v1 as components

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
    for a, b in {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
    }.items():
        texto = texto.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", texto).strip("_")


# === FUNCIÓN CORREGIDA: ENRUTAMIENTO DIRECTO PYODBC ===
def obtener_datos_liquidaciones_sql():
    """Conecta a la base de datos SQL de Express San Silvestre usando pyodbc y extrae las liquidaciones."""
    servidor = "gmterpbi.database.windows.net"
    base_datos = "GMTERP_BI_ESS970424CS1"
    usuario = "admin@SanSilvestreAllende.onmicrosoft.com"
    contrasena = "LewnAYYq5;."

    # Cadena limpia con concatenación estándar
    cadena_conexion = (
        "DRIVER={SQL Server};"
        "SERVER=" + servidor + ";"
        "DATABASE=" + base_datos + ";"
        "UID=" + usuario + ";"
        "PWD=" + contrasena + ";"
        "Authentication=ActiveDirectoryPassword;"
    )

    # Query unificado que calcula cada medida DAX basándose en sus filtros de 'SubConcepto'
    query = """
        SELECT 
            l.Folio,
            l.Codigo AS Unidad,
            l.Nombre,
            l.CreadoEl,
            l.Creo,
            l.Ingresos,
            
            -- 1. Gastos Extras (Medida Original)
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) IN (
                'TRANSITO', 'COMPRA DE LLANTA', 'REFACCIONES', 'SUPERVISOR', 
                'TALACHAS', 'MOVIMIENTOS PENDIENTES', 'GUIA', 'TRANSITO RECUPERABLE', 
                'ACEITE', 'GATAS'
            ) THEN e.Total ELSE 0 END), 0) AS Gastos_Extras,

            -- 2. Sobresueldos (BONOS, VIATICOS)
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) IN (
                'BONOS', 'VIATICOS'
            ) THEN e.Total ELSE 0 END), 0) AS Sobresueldos,

            -- 3. G Pre Aut (ESTANCIA, REPARTOS, etc.)
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) IN (
                'ESTANCIA', 'REPARTOS (SORIANA)', 'LAVADA THERMO', 
                'ENTRADA MERCADO', 'PENSION', 'LONAS FULL'
            ) THEN e.Total ELSE 0 END), 0) AS G_Pre_Aut,

            -- 4. G Pre Aut / OP (FITOSANITARIA, PERMISO DE TRANSITO, etc.)
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) IN (
                'FITOSANITARIA', 'PERMISO DE TRANSITO', 'TRANSFER', 'COMISIONES'
            ) THEN e.Total ELSE 0 END), 0) AS G_Pre_Aut_OP,

            -- Desglose por columnas individuales para el Excel resultante
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'COMPRA DE LLANTA' THEN e.Total ELSE 0 END), 0) AS Gasto_Compra_de_Llanta,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'MOVIMIENTOS PENDIENTES' THEN e.Total ELSE 0 END), 0) AS Gasto_Movimientos_Pendientes,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'REFACCIONES' THEN e.Total ELSE 0 END), 0) AS Gasto_Refacciones,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'TALACHAS' THEN e.Total ELSE 0 END), 0) AS Gasto_Talachas,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'GATAS' THEN e.Total ELSE 0 END), 0) AS Gasto_Gatas,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'GUIA' THEN e.Total ELSE 0 END), 0) AS Gasto_Guia,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'SUPERVISOR' THEN e.Total ELSE 0 END), 0) AS Gasto_Supervisor,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'TRANSITO' THEN e.Total ELSE 0 END), 0) AS Gasto_Transito,
            COALESCE(SUM(CASE WHEN TRIM(UPPER(e.SubConcepto)) = 'TRANSITO RECUPERABLE' THEN e.Total ELSE 0 END), 0) AS Gasto_Transito_Recuperable

        FROM liquidaciones l
        LEFT JOIN ViajesTrayectos vt ON vt.IdLiquidacion = l.IdLiquidacion
        LEFT JOIN EgresosViajes e ON e.IDViaje = vt.IDViaje
        GROUP BY l.IdLiquidacion, l.Folio, l.Codigo, l.Nombre, l.CreadoEl, l.Creo, l.Ingresos
    """
    
    # Abrimos la conexión física utilizando pyodbc de forma explícita
    conexion = pyodbc.connect(cadena_conexion)
    
    # Pasamos el objeto de conexión en lugar de la cadena de texto para omitir SQLAlchemy
    df = pd.read_sql(query, conexion)
    
    # Cerramos la conexión activa
    conexion.close()
    
    # --- PROCESAMIENTO PANDAS (Equivalente a tus medidas DAX compuestas) ---
    df['Gastos_OK'] = df['Gastos_Extras'] + df['Sobresueldos'] + df['G_Pre_Aut'] + df['G_Pre_Aut_OP']
    
    df['Porcentaje_Gastos_Extras'] = (df['Gastos_Extras'] / df['Ingresos'].replace(0, np.nan)) * 100
    df['Porcentaje_Gastos_Extras'] = df['Porcentaje_Gastos_Extras'].fillna(0).round(2)
    
    df['Porcentaje_Total_Gastos'] = (df['Gastos_OK'] / df['Ingresos'].replace(0, np.nan)) * 100
    df['Porcentaje_Total_Gastos'] = df['Porcentaje_Total_Gastos'].fillna(0).round(2)
    
    return df


# === CONFIGURACIÓN DEL CARRUSEL DE INICIO ===
RUTA_CARRUSEL = "assets/carousel"


def imagen_a_base64(ruta: str) -> str:
    """Lee una imagen local y la convierte en data-URI base64 para incrustarla en HTML."""
    extension = Path(ruta).suffix.replace(".", "").lower()
    extension = "jpeg" if extension == "jpg" else extension
    with open(ruta, "rb") as archivo:
        datos = base64.b64encode(archivo.read()).decode()
    return f"data:image/{extension};base64,{datos}"


def obtener_imagenes_carrusel(carpeta: str) -> list:
    """Devuelve, en base64, todas las imágenes válidas encontradas en `carpeta`."""
    carpeta_path = Path(carpeta)
    if not carpeta_path.exists():
        return []
    extensiones_validas = {".jpg", ".jpeg", ".png", ".webp"}
    archivos = sorted(
        p for p in carpeta_path.iterdir() if p.suffix.lower() in extensiones_validas
    )
    imagenes = []
    for archivo in archivos:
        try:
            imagenes.append(imagen_a_base64(str(archivo)))
        except Exception:
            continue
    return imagenes


# === CONFIGURACIÓN DE TABLEROS POWER BI ===
REPORTES_POWERBI = {
    "Capital Humano": "https://app.powerbi.com/view?r=eyJrIjoiNmU0MTg2NjUtMGQ1My00MjU4LWE5ODgtZTBjY2NjMTE0YjYxIiwidCI6IjFmYzUzMTA5LTZhMDAtNGExZi1hNmJjLTdkZGZkNGIzZGRjZiJ9&pageName=1528e6a9ffef26f42f39",
    "Comercial": "https://app.powerbi.com/view?r=eyJrIjoiMDM4ZjMwN2EtOThlOS00ODI5LWEyNTEtOGE2NjhjZDQ2MTk5IiwidCI6IjFmYzUzMTA5LTZhMDAtNGExZi1hNmJjLTdkZGZkNGIzZGRjZiJ9&pageName=36d5c229a0939c8234c4",
    "Liquidaciones": "https://app.powerbi.com/view?r=eyJrIjoiMjlhOTNhYTAtOGI3OC00YTg2LTkxMTMtYjM5YmI4NmM5MDNhIiwidCI6IjFmYzUzMTA5LTZhMDAtNGExZi1hNmJjLTdkZGZkNGIzZGRjZiJ9&pageName=18f7891f4ced9ea3a7e9",
    "Operaciones": "https://app.powerbi.com/view?r=eyJrIjoiZDZiYjIxMGUtNDlmOS00MGVhLTgwODYtMGE5NGJiNzhmMzE3IiwidCI6IjFmYzUzMTA5LTZhMDAtNGExZi1hNmJjLTdkZGZkNGIzZGRjZiJ9&pageName=7c18946f915bd493ad4b",
    "Flotilla": "https://app.powerbi.com/view?r=eyJrIjoiNDUzMDUwNjAtZDRiMy00ZjQwLWI0ZGEtMGM3NTVmNWY1YTZmIiwidCI6IjFmYzUzMTA5LTZhMDAtNGExZi1hNmJjLTdkZGZkNGIzZGRjZiJ9",
    "Códigos de Falla": "https://app.powerbi.com/view?r=eyJrIjoiOTBhZTcxMjQtMWQwOS00OTE4LTgzNGUtMDgzMWYyOTU3YTgwIiwidCI6IjFmYzUzMTA5LTZhMDAtNGExZi1hNmJjLTdkZGZkNGIzZGRjZiJ9",
}


def mostrar_tablero_powerbi(url: str, alto: int = 650):
    if not url:
        st.markdown(
            '<div class="info-card-custom">⚠️ Este tablero todavía no tiene una URL '
            "de Power BI configurada. Pégala en el diccionario "
            "<code>REPORTES_POWERBI</code> dentro del código.</div>",
            unsafe_allow_html=True,
        )
        return
    components.iframe(url, height=alto, scrolling=True)


def construir_carrusel_html(
    imagenes_b64, titulo, subtitulo, kpis=None, alto=380, intervalo_ms=4500
):
    if imagenes_b64:
        slides_html = "".join(
            f'<div class="hero-slide{" active" if i == 0 else ""}" '
            f"style=\"background-image:url('{img}')\"></div>"
            for i, img in enumerate(imagenes_b64)
        )
        dots_html = "".join(
            f'<span class="{"active" if i == 0 else ""}"></span>'
            for i in range(len(imagenes_b64))
        )
        mostrar_dots = len(imagenes_b64) > 1
    else:
        slides_html = '<div class="hero-slide active sin-imagen"></div>'
        dots_html = ""
        mostrar_dots = False

    kpis_html = ""
    if kpis:
        kpis_html = "".join(
            f'<div class="kpi-item"><div class="kpi-num">{num}</div>'
            f'<div class="kpi-label">{label}</div></div>'
            for num, label in kpis
        )

    return f"""
    <style>
        * {{ box-sizing: border-box; font-family: 'Segoe UI', Arial, sans-serif; }}
        body {{ margin: 0; }}
        .hero-carousel {{
            position: relative;
            width: 100%;
            height: {alto}px;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0px 12px 30px rgba(20, 20, 60, 0.25);
        }}
        .hero-slide {{
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center;
            opacity: 0;
            transition: opacity 1.4s ease-in-out;
        }}
        .hero-slide.active {{ opacity: 1; }}
        .hero-slide.sin-imagen {{
            background: linear-gradient(135deg, #12123A 0%, #2A2E8F 55%, #4B4FE8 100%);
        }}
        .hero-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(8,8,35,0.20) 0%, rgba(6,6,28,0.88) 100%);
        }}
        .hero-dots {{
            position: absolute;
            top: 22px;
            right: 26px;
            z-index: 2;
            display: flex;
            gap: 7px;
        }}
        .hero-dots span {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: rgba(255,255,255,0.35);
            transition: background 0.3s ease;
        }}
        .hero-dots span.active {{ background: #FFFFFF; }}
        .hero-content {{
            position: absolute;
            left: 42px;
            right: 42px;
            bottom: 32px;
            z-index: 2;
            color: #FFFFFF;
        }}
        .hero-content h2 {{
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin: 0 0 8px 0;
            text-shadow: 0px 2px 10px rgba(0,0,0,0.35);
        }}
        .hero-content p {{
            font-size: 0.98rem;
            color: rgba(255,255,255,0.85);
            margin: 0 0 22px 0;
            max-width: 620px;
            line-height: 1.5;
        }}
        .hero-kpis {{
            display: flex;
            gap: 40px;
            border-top: 1px solid rgba(255,255,255,0.18);
            padding-top: 16px;
        }}
        .kpi-num {{
            font-size: 1.35rem;
            font-weight: 800;
        }}
        .kpi-label {{
            font-size: 0.7rem;
            color: rgba(255,255,255,0.65);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 2px;
        }}
    </style>

    <div class="hero-carousel">
        {slides_html}
        <div class="hero-overlay"></div>
        {'<div class="hero-dots">' + dots_html + '</div>' if mostrar_dots else ''}
        <div class="hero-content">
            <h2>{titulo}</h2>
            <p>{subtitulo}</p>
            {'<div class="hero-kpis">' + kpis_html + '</div>' if kpis_html else ''}
        </div>
    </div>

    <script>
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.hero-dots span');
        let idx = 0;
        if (slides.length > 1) {{
            setInterval(() => {{
                slides[idx].classList.remove('active');
                if (dots[idx]) dots[idx].classList.remove('active');
                idx = (idx + 1) % slides.length;
                slides[idx].classList.add('active');
                if (dots[idx]) dots[idx].classList.add('active');
            }}, {intervalo_ms});
        }}
    </script>
    """


# === INYECCIÓN CSS ULTRA-ESTRICTA Y GLOBAL ===
slug_seleccionado = slugify(st.session_state.menu_seleccionado)

st.markdown(
    f"""
    <style>
        [data-testid="stSidebar"] {{
            background-color: #0E0E3A !important;
        }}
        [data-testid="stSidebarCollapseButton"] button {{
            background-color: rgba(255, 255, 255, 0.10) !important;
            border-radius: 8px !important;
            opacity: 1 !important;
        }}
        [data-testid="stSidebarCollapseButton"] svg {{
            fill: #FFFFFF !important;
            opacity: 1 !important;
            width: 22px !important;
            height: 22px !important;
        }}
        [data-testid="stSidebarCollapseButton"] button:hover {{
            background-color: rgba(255, 255, 255, 0.2) !important;
        }}
        [data-testid="stSidebarContent"] {{
            display: flex !important;
            flex-direction: column !important;
            height: 100vh !important;
            padding-top: 10px !important;
            padding-bottom: 20px !important;
        }}
        .menu-titulo-custom {{
            color: rgba(255, 255, 255, 0.35) !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            margin: 10px 0 10px 14px !important;
            display: block !important;
        }}
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
        [data-testid="stSidebar"] [data-testid="stButton"] button:hover {{
            background-color: rgba(255, 255, 255, 0.07) !important;
            color: #FFFFFF !important;
        }}
        .st-key-menu_{slug_seleccionado} button {{
            background-color: #4B4FE8 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            box-shadow: 0px 4px 10px rgba(75, 79, 232, 0.35) !important;
        }}
        .sidebar-divider {{
            border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
            margin: 8px 14px 6px 14px !important;
        }}
        .sidebar-leyenda {{
            color: rgba(255, 255, 255, 0.30) !important;
            font-size: 0.7rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            text-align: center !important;
            margin: 0 0 4px 0 !important;
            display: block !important;
        }}
        .sidebar-bottom-container {{
            margin-top: auto !important;
            display: flex !important;
            flex-direction: column !important;
        }}
        .sidebar-bottom-spacer {{
            flex-grow: 1 !important;
            min-height: 24px !important;
        }}
        .sidebar-bottom-container [data-testid="stButton"] button:hover {{
            background-color: rgba(211, 47, 47, 0.18) !important;
            color: #FF6B6B !important;
        }}
        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
            border: 1px solid #CCCCCC !important;
        }}
        .stTextInput label {{
            color: #1A1A1A !important;
        }}
        [data-testid="stAppViewContainer"] {{
            background-color: #F3F4FA !important;
        }}
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        .block-container {{
            padding-top: 2.2rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
            max-width: 1180px !important;
        }}
        h1 {{
            color: #14153A !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }}
        .subtitulo-portal {{
            color: #5B5E7A !important;
            font-size: 1.02rem !important;
            margin-top: -10px !important;
            margin-bottom: 1.4rem !important;
        }}
        h3 {{
            color: #1E1F45 !important;
            font-weight: 700 !important;
        }}
        .info-card-custom {{
            background-color: #FFFFFF !important;
            border-left: 4px solid #4B4FE8 !important;
            border-radius: 10px !important;
            padding: 16px 20px !important;
            box-shadow: 0px 6px 18px rgba(20, 20, 60, 0.06) !important;
            color: #33354D !important;
            font-size: 0.92rem !important;
            line-height: 1.55 !important;
            margin-top: 1rem !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


def obtener_credenciales():
    try:
        return st.secrets["auth"]["usuario"], st.secrets["auth"]["contrasena"]
    except Exception:
        return "admin", "ess2026"


def verificar_login(usuario, contrasena):
    usuario_valido, contrasena_valida = obtener_credenciales()
    if usuario == usuario_valido and contrasena == contrasena_valida:
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
    st.sidebar.markdown(
        '<span class="menu-titulo-custom">Módulos de Análisis</span>',
        unsafe_allow_html=True,
    )

    opciones_menu = {
        "Inicio": ("🏠", "Inicio"),
        "Capital Humano": ("👥", "Capital Humano"),
        "Comercial": ("💼", "Comercial y Ventas"),
        "Liquidaciones": ("🧮", "Liquidaciones"),
        "Operaciones": ("⚙️", "Operaciones"),
        "Flotilla": ("🚛", "Flotilla y Activos"),
        "Códigos de Falla": ("⚠️", "Códigos de Falla"),
    }

    for clave, (icono, etiqueta) in opciones_menu.items():
        slug = slugify(clave)
        with st.sidebar.container(key=f"menu_{slug}"):
            if st.button(f"{icono}  {etiqueta}", key=f"btn_{slug}"):
                st.session_state.menu_seleccionado = clave
                st.rerun()

    with st.sidebar:
        st.sidebar.markdown('<div class="sidebar-bottom-container">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.sidebar.markdown('<span class="sidebar-leyenda">Desarrollo De Datos</span>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-bottom-spacer"></div>', unsafe_allow_html=True)
        if st.button("🚪  Cerrar Sesión", key="btn_logout"):
            st.session_state.autenticado = False
            st.session_state.menu_seleccionado = "Inicio"
            st.rerun()
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # === Área Principal de Contenidos ===
    st.title("Express San Silvestre")
    st.markdown(
        '<p class="subtitulo-portal">Bienvenido al centro de mando de datos de la organización.</p>',
        unsafe_allow_html=True,
    )

    area = st.session_state.menu_seleccionado

    if area == "Inicio":
        imagenes_hero = obtener_imagenes_carrusel(RUTA_CARRUSEL)
        html_hero = construir_carrusel_html(
            imagenes_b64=imagenes_hero,
            titulo="Bienvenido al Portal de BI - ESS",
            subtitulo="Selecciona un módulo en la barra lateral para inicializar los tableros analíticos.",
        )
        components.html(html_hero, height=400)

        st.markdown(
            """
            <div class="info-card-custom">
                Nota corporativa: Para la descarga o extracción de registros optimizados 
                con métricas DAX, localice las herramientas de exportación dispuestas en 
                la base de cada sección correspondiente.
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif area == "Capital Humano":
        st.subheader("👥 Indicadores de Capital Humano")
        mostrar_tablero_powerbi(REPORTES_POWERBI["Capital Humano"])

    elif area == "Comercial":
        st.subheader("💼 Tablero Comercial y Ventas")
        mostrar_tablero_powerbi(REPORTES_POWERBI["Comercial"])

    elif area == "Liquidaciones":
        st.subheader("🧮 Módulo de Liquidaciones")
        mostrar_tablero_powerbi(REPORTES_POWERBI["Liquidaciones"])

        # --- EXTRACCIÓN Y EXPORTACIÓN A EXCEL DESDE SQL ---
        st.markdown("---")
        try:
            # 1. Traemos los datos frescos desde SQL con las nuevas medidas incorporadas
            df_liq = obtener_datos_liquidaciones_sql()

            # 2. Convertimos el DataFrame a un archivo Excel binario
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df_liq.to_excel(writer, index=False, sheet_name="Liquidaciones")
            excel_data = output.getvalue()

            # 3. Dibujamos el botón de descarga abajo del Power BI
            st.download_button(
                label="📥 Descargar Detalle de Liquidaciones en Excel (.xlsx)",
                data=excel_data,
                file_name="Detalle_Liquidaciones_Operadores.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as error_sql:
            st.error(
                f"No se pudieron extraer los registros de SQL en tiempo real: {error_sql}"
            )

    elif area == "Operaciones":
        st.subheader("⚙️ Control de Operaciones")
        mostrar_tablero_powerbi(REPORTES_POWERBI["Operaciones"])

    elif area == "Flotilla":
        st.subheader("🚛 Gestión de Flotilla y Activos")
        mostrar_tablero_powerbi(REPORTES_POWERBI["Flotilla"])

    elif area == "Códigos de Falla":
        st.subheader("⚠️ Análisis de Códigos de Falla")
        mostrar_tablero_powerbi(REPORTES_POWERBI["Códigos de Falla"])
