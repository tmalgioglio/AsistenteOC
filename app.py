import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import unicodedata

# 1. CONFIGURACIÓN DE LA PÁGINA (Estética Vercel/Apple)
st.set_page_config(
    page_title="Asistente de Operaciones Comerciales",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Cargar estilos CSS personalizados
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"No se encontró el archivo de estilos {file_name}")

local_css("styles.css")

# 2. BASE DE DATOS DE RESPALDO (Fallbacks / Demo Mode)
DEFAULT_DATA = [
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Solicitud de Mochilas Comerciales", "URL": "https://docs.google.com/forms/d/e/1FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Solicitud Nuevo Titular de Zona de Venta", "URL": "https://docs.google.com/forms/d/e/2FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Seguimiento Reemplazos Fuerza de Venta", "URL": "https://lookerstudio.google.com/reporting/reemplazos"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "HOGAR | Solicitud de Categorización/Descategorización", "URL": "https://docs.google.com/forms/d/e/3FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Hogar | Solicitud de Categoría y/o MV por Cambio de Razón Social", "URL": "https://docs.google.com/forms/d/e/4FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "HOGAR | Solicitud Cliente Consolidador", "URL": "https://docs.google.com/forms/d/e/5FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "HORECA | Solicitud Cliente Consolidador", "URL": "https://docs.google.com/forms/d/e/6FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Solicitud - Modificación Cliente responsable de Pago", "URL": "https://docs.google.com/forms/d/e/7FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Solicitud de Asociación Unidad/Conductor", "URL": "https://docs.google.com/forms/d/e/8FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Solicitud Alta de Camión", "URL": "https://docs.google.com/forms/d/e/9FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "Google Forms", "Tramite": "Corrientes || Solicitud Afectación a incobrables", "URL": "https://docs.google.com/forms/d/e/10FAIpQLSfP8eXy0A7yNdf4328h9s/viewform"},
    {"Sucursal": "Todas", "Herramienta": "SAP", "Tramite": "Manuales y Capacitaciones", "URL": "https://sap.lavirginia.com.ar/capacitaciones"},
    {"Sucursal": "Todas", "Herramienta": "SAP", "Tramite": "Acceso SAP Analytics Cloud", "URL": "https://sap.lavirginia.com.ar/sac"},
    {"Sucursal": "02 - Rosario", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/rosario-carga-acuerdos"},
    {"Sucursal": "02 - Rosario", "Herramienta": "Monday", "Tramite": "Solicitud de ejecucion de Acuerdos", "URL": "https://monday.com/boards/rosario-ejecucion-acuerdos"},
    {"Sucursal": "03 - Santa Fe", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/santafe-carga-acuerdos"},
    {"Sucursal": "03 - Santa Fe", "Herramienta": "Monday", "Tramite": "Solicitud de ejecucion de Acuerdos", "URL": "https://monday.com/boards/santafe-ejecucion-acuerdos"},
    {"Sucursal": "04 - Resistencia", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/resistencia-carga"},
    {"Sucursal": "05 - Posadas", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/posadas-carga"},
    {"Sucursal": "07 - Córdoba", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/cordoba-carga"},
    {"Sucursal": "07 - Córdoba", "Herramienta": "Monday", "Tramite": "Solicitud de ejecucion de Acuerdos", "URL": "https://monday.com/boards/cordoba-ejecucion"},
    {"Sucursal": "10 - Concordia", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/concordia-carga"},
    {"Sucursal": "11 - Santiago", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/santiago-carga"},
    {"Sucursal": "12 - Bahía Blanca", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/bahia-carga"},
    {"Sucursal": "13 - Salta", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/salta-carga"},
    {"Sucursal": "15 - Mendoza", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/mendoza-carga"},
    {"Sucursal": "16 - Tucumán", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/tucuman-carga"},
    {"Sucursal": "17 - GBA", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/gba-carga"},
    {"Sucursal": "18 - Mar del Plata", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/mdp-carga"},
    {"Sucursal": "20 - Neuquén", "Herramienta": "Monday", "Tramite": "Carga de Acuerdos", "URL": "https://monday.com/boards/neuquen-carga"}
]

# 3. LECTURA DE DATOS CON CACHÉ INTELIGENTE (Google Sheets CSV)
@st.cache_data(ttl=900)  # 15 minutos de TTL
def load_sheet_data(sheet_url=None):
    if not sheet_url:
        return pd.DataFrame(DEFAULT_DATA), True # Demo mode flag = True
    try:
        df = pd.read_csv(sheet_url)
        # Limpieza básica de columnas para evitar fallas
        required_cols = {"Sucursal", "Herramienta", "Tramite", "URL"}
        if not required_cols.issubset(df.columns):
            st.error(f"El Google Sheet debe contener las columnas: {required_cols}")
            return pd.DataFrame(DEFAULT_DATA), True
        return df, False
    except Exception as e:
        st.warning(f"No se pudo cargar el Google Sheet. Usando base de datos interna. Detalle: {e}")
        return pd.DataFrame(DEFAULT_DATA), True

# Función para obtener secretos de forma segura
def get_secret(key, default=None):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return os.environ.get(key, default)

# Determinar URL del Google Sheet
# Se lee de st.secrets o de variables de entorno
sheet_url = get_secret("GOOGLE_SHEET_URL", None)
df_links, is_demo_mode = load_sheet_data(sheet_url)

# 4. GESTIÓN DE ESTADO (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_branch" not in st.session_state:
    st.session_state.user_branch = None

if "api_key" not in st.session_state:
    # Intenta obtener la API key de los secretos de Streamlit
    st.session_state.api_key = get_secret("GEMINI_API_KEY", "")

# 5. HEADER Y TITULAR
st.markdown("""
<div class="header-container">
    <div class="brand-badge">LA VIRGINIA • OPERACIONES</div>
    <div class="header-title">Asistente de Operaciones Comerciales</div>
    <div class="header-subtitle">Buscá de forma ágil planillas, herramientas y accesos para tu sucursal.</div>
</div>
""", unsafe_allow_html=True)

# Indicador sutil de base de datos
if is_demo_mode:
    st.toast("Modo Demo: Cargado con base de datos interna de respaldo.", icon="💡")

# Widget de Sucursal Actual
if st.session_state.user_branch:
    col_badge, col_reset = st.columns([4, 1])
    with col_badge:
        st.markdown(f"📍 Sucursal activa: **{st.session_state.user_branch}**", unsafe_allow_html=True)
    with col_reset:
        if st.button("Cambiar ↩", key="reset_branch_btn", help="Hacé clic para cambiar la sucursal"):
            st.session_state.user_branch = None
            st.rerun()
    st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0; border: 0; border-top: 1px solid #eaeaea;'>", unsafe_allow_html=True)

# 6. CONFIGURACIÓN DE LA API KEY DE GEMINI (Si no está configurada)
if not st.session_state.api_key:
    st.markdown("""
    <div class="chat-bubble assistant-bubble" style="max-width: 100%;">
        🔑 <strong>Configuración Inicial de Gemini API Key:</strong><br>
        Para comenzar a chatear, por favor introduce tu clave de API de Gemini. 
        Puedes obtener una gratis en <a href="https://aistudio.google.com/" target="_blank">Google AI Studio</a>.
    </div>
    """, unsafe_allow_html=True)
    
    api_key_input = st.text_input("Ingresá tu API Key de Gemini:", type="password", key="api_key_field")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.rerun()
    st.stop()

# Configurar SDK de Gemini
genai.configure(api_key=st.session_state.api_key)

# 7. LOGICA DE DETECCION DE SUCURSAL EN TEXTO
def detect_branch_in_text(text, branches):
    """
    Escanea el texto del usuario para buscar menciones de sucursales conocidas.
    """
    def clean_string(s):
        s = s.lower()
        s = "".join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )
        return s

    cleaned_text = clean_string(text)
    
    for branch in branches:
        if branch.lower() == 'todas':
            continue
        # Limpieza del nombre de la sucursal (ej: "02 - Rosario" -> "rosario")
        branch_name = branch.split(" - ", 1)[1] if " - " in branch else branch
        cleaned_branch = clean_string(branch_name)
        
        # Validación del match (ej. si el usuario escribe "rosario" y coincide con "rosario")
        if cleaned_branch in cleaned_text:
            return branch
            
    return None

# Obtener lista única de sucursales
unique_branches = df_links["Sucursal"].unique()

# 8. HISTORIAL DE MENSAJES (Visualización)
for message in st.session_state.messages:
    role_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="chat-bubble {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# 9. SUGERENCIAS DE INICIO RÁPIDO
if len(st.session_state.messages) == 0:
    st.markdown('<p style="text-align: center; color: #71717a; font-size: 0.85rem; margin-bottom: 0.5rem; font-weight: 500;">Preguntas sugeridas:</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    suggestions = [
        ("📦 Mochilas Comerciales", "Necesito el link para Solicitud de Mochilas Comerciales"),
        ("📝 Carga de Acuerdos", "Pasame el enlace para Carga de Acuerdos"),
        ("🚛 Alta de Camión", "Quiero registrar un Alta de Camión"),
        ("💻 Acceso a SAP", "Manuales y accesos de SAP")
    ]
    for i, (label, prompt) in enumerate(suggestions):
        with cols[i % 4]:
            if st.button(label, key=f"sug_{i}", use_container_width=True):
                # Guardar el mensaje del usuario y gatillar re-run
                st.session_state.messages.append({"role": "user", "content": prompt})
                # Auto-detectar sucursal si el prompt de sugerencia es procesado
                detected = detect_branch_in_text(prompt, unique_branches)
                if detected:
                    st.session_state.user_branch = detected
                st.rerun()

# 10. ENTRADA DE CHAT
user_prompt = st.chat_input("Escribí tu mensaje acá... (ej. Carga de acuerdos Rosario)")
if user_prompt:
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    # Detectar si hay sucursal
    detected_branch = detect_branch_in_text(user_prompt, unique_branches)
    if detected_branch:
        st.session_state.user_branch = detected_branch
    st.rerun()

# 11. RESPUESTA DEL ASISTENTE (Si el último mensaje es del usuario)
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    # Usar un contenedor temporal para el spinner y el mensaje del asistente
    with st.chat_message("assistant"):
        with st.spinner("Procesando consulta..."):
            # Preparar contexto (Database en formato lista concisa)
            db_context = ""
            for _, row in df_links.iterrows():
                db_context += f"- Sucursal: {row['Sucursal']} | Herramienta: {row['Herramienta']} | Trámite: {row['Tramite']} | URL: {row['URL']}\n"

            # Formatear sucursal actual
            branch_status = st.session_state.user_branch if st.session_state.user_branch else "Desconocida"

            # Generar System Instruction
            system_prompt = f"""
            Eres el Asistente Virtual de Operaciones Comerciales de la empresa La Virginia. Tu objetivo es ayudar al personal de las sucursales a encontrar rápidamente los enlaces (URLs) que necesitan.

            REGLAS DE COMPORTAMIENTO:
            1. TONO: Sé sumamente conciso, profesional, servicial y directo. No des rodeos ni explicaciones largas. Usa español de Argentina de forma natural pero profesional (ej. "decime", "acá tenés el link").
            2. SUCURSAL DEL USUARIO ACTUAL: "{branch_status}"
            3. DETECCIÓN DE SUCURSAL:
               - Si el trámite solicitado depende de la sucursal (ej: Carga de Acuerdos, Solicitud de ejecución) y la sucursal actual es "Desconocida", DEBES pedir amablemente al usuario que te diga de qué sucursal es (ej. "¿De qué sucursal sos?"). No muestres ningún link de sucursal hasta saberla.
               - Si el trámite es general (Sucursal: "Todas"), entrega el link directamente sin importar la sucursal.
               - Si la sucursal ya es conocida (distinta de "Desconocida"), entrega DIRECTAMENTE el enlace que le corresponde a esa sucursal específica.
            4. CÓMO ENTREGAR ENLACES:
               - Cuando entregues un enlace, hazlo en su propia línea usando Markdown estándar: [Nombre del Trámite o Herramienta](URL). La aplicación se encargará de darle diseño de botón.
               - El texto que acompaña al link debe ser muy corto (ej: "Acá tenés el link para la carga de acuerdos en Rosario:").
            
            BASE DE DATOS DE LINKS AUTORIZADA:
            {db_context}
            """

            try:
                # Inicializar modelo de Gemini con system instructions
                model = genai.GenerativeModel(
                    model_name="gemini-3.5-flash",
                    system_instruction=system_prompt,
                    generation_config={"temperature": 0.1} # Baja temperatura para evitar alucinaciones
                )

                # Convertir historial de Streamlit al formato de la API de Gemini
                contents = []
                for msg in st.session_state.messages:
                    contents.append({
                        "role": "user" if msg["role"] == "user" else "model",
                        "parts": [msg["content"]]
                    })

                # Obtener respuesta de Gemini
                response = model.generate_content(contents)
                assistant_response = response.text

                # Guardar respuesta del asistente
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                st.rerun()

            except Exception as e:
                st.error(f"Ocurrió un error al consultar con el asistente: {e}")
