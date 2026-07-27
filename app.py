# Esto NO se sube a GitHub. Es solo un ejemplo de lo que debes pegar
# en Streamlit Cloud: tu app > Settings > Secrets.

# --- Conexión a la API de Power BI (Portals-ESS Reportes) ---
POWERBI_TENANT_ID = "1fc53109-6a00-4a1f-a6bc-7ddfd4b3ddcf"
POWERBI_CLIENT_ID = "fe23a732-047e-45b8-b617-b34f6ac298a3"
POWERBI_USER = "cuenta_de_servicio@expresssansilvestre.com"
POWERBI_PASSWORD = "clave_de_esa_cuenta"

# --- Usuarios del portal y las áreas que cada uno puede ver ---
# "Inicio" siempre es visible para todos aunque no lo listes.
# Los nombres de área deben coincidir EXACTO con las claves de opciones_menu
# en el código: Capital Humano, Comercial, Liquidaciones, Operaciones,
# Flotilla, Códigos de Falla.

[usuarios.admin]
contrasena = "CambiaEstaClaveSegura2026"
areas = ["Capital Humano", "Comercial", "Liquidaciones", "Operaciones", "Flotilla", "Códigos de Falla"]

[usuarios.operaciones1]
contrasena = "ClaveOperaciones2026"
areas = ["Operaciones"]

[usuarios.rh1]
contrasena = "ClaveRH2026"
areas = ["Capital Humano"]

[usuarios.liquidaciones1]
contrasena = "ClaveLiq2026"
areas = ["Liquidaciones"]
