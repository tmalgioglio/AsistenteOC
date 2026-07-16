# Asistente Virtual de Operaciones Comerciales - La Virginia

Este es el repositorio del asistente conversacional de operaciones comerciales desarrollado para la empresa **La Virginia**. Permite reemplazar las intranets tradicionales por una experiencia fluida, minimalista y de alta conversión integrada en Google Sites.

---

## 🏛️ Estructura del Proyecto

*   `app.py`: Archivo de la aplicación Streamlit con lógica de inyección de contexto y llamadas al SDK de Gemini.
*   `styles.css`: Estilos personalizados de diseño premium ("Vercel / Apple") con la paleta corporativa moderna.
*   `requirements.txt`: Lista de dependencias de Python necesarias para correr el asistente.

---

## 📊 1. Configuración de Google Sheets (Base de Datos CMS)

Para administrar la base de datos de enlaces dinámicamente y permitir que los administradores actualicen links sin tocar el código:

1.  Crea una planilla en **Google Sheets** con las siguientes columnas exactas en la primera fila:
    *   `Sucursal` (ej. `Todas`, `02 - Rosario`, `03 - Santa Fe`, etc.)
    *   `Herramienta` (ej. `Monday`, `Google Forms`, `SAP`)
    *   `Tramite` (ej. `Carga de Acuerdos`, `Solicitud de Mochilas Comerciales`)
    *   `URL` (ej. `https://monday.com/boards/...` o `https://docs.google.com/forms/...`)
    *   `Destacado` (Opcional. Valores: `SI` o vacío. Permite forzar a que este trámite aparezca en las píldoras de "Preguntas sugeridas" en el inicio del chat).
2.  Agrega las filas de datos correspondientes a tus sucursales y trámites.
3.  Ve al menú **Archivo** (File) > **Compartir** (Share) > **Publicar en la Web** (Publish to the Web).
4.  En la ventana flotante:
    *   Selecciona la hoja de trabajo específica (ej. "Hoja 1").
    *   Cambia la opción **Página Web** (Web Page) por **Valores separados por comas (.csv)** (Comma-separated values).
5.  Haz clic en el botón **Publicar** (Publish) y confirma la acción.
6.  **Copia el enlace generado**. Debería tener un formato similar a este:
    `https://docs.google.com/spreadsheets/d/1FAIpQLSf.../pub?output=csv`

---

## ☁️ 2. Despliegue en Streamlit Community Cloud (Gratis)

1.  Sube los archivos (`app.py`, `styles.css`, `requirements.txt`) a un repositorio público en tu cuenta de **GitHub**.
2.  Ingresa a [Streamlit Community Cloud](https://share.streamlit.io/) e inicia sesión con tu cuenta de GitHub.
3.  Haz clic en el botón **New app** (Nueva aplicación).
4.  Configura los campos:
    *   **Repository:** Tu repositorio de GitHub.
    *   **Branch:** `main` (o la rama que uses).
    *   **Main file path:** `app.py`.
5.  Haz clic en **Advanced settings...** (Configuración avanzada) antes de desplegar para definir los Secretos:
    *   En el área de texto de **Secrets** (en formato TOML), ingresa tus credenciales y el enlace del Excel:
        ```toml
        GEMINI_API_KEY = "TU_API_KEY_DE_GEMINI"
        GOOGLE_SHEET_URL = "URL_DE_TU_CSV_DE_GOOGLE_SHEETS"
        ```
    *   *(Nota: Puedes obtener una API Key de Gemini gratis en [Google AI Studio](https://aistudio.google.com/))*.
6.  Haz clic en **Save** y luego en **Deploy!**. Streamlit compilará e iniciará tu aplicación en unos minutos.

---

## 🎨 3. Integración en Google Sites

Para insertar el asistente en una sección dedicada a pantalla completa en tu Google Sites:

1.  Copia la URL pública de tu aplicación Streamlit desplegada (ej. `https://la-virginia-ops.streamlit.app`).
2.  Añade el parámetro de embebido nativo de Streamlit al final de la URL: `?embed=true`.
    *   Ejemplo: `https://la-virginia-ops.streamlit.app/?embed=true`
    *   *(Este parámetro limpia la pantalla eliminando menús y barras superfluas de Streamlit, adaptando el chat a iframe).*
3.  Ve al editor de tu **Google Sites**.
4.  En la barra lateral derecha, selecciona la pestaña **Insertar** (Insert) y haz clic en **Incrustar** (Embed).
5.  Pega la URL modificada en la pestaña **Mediante URL** (By URL).
6.  Ajusta el tamaño del contenedor en Google Sites arrastrando los bordes para que ocupe todo el ancho y alto de la página de forma cómoda.
7.  Haz clic en **Publicar** en Google Sites. ¡Tu asistente ya está listo para todas las sucursales!

---

## ⚙️ 4. Preguntas Frecuentes y Lógica de Desarrollo

### ¿El CSV se mantiene actualizado automáticamente?
**Sí.** Al usar "Publicar en la web" de Google Sheets, Google sirve el archivo CSV actualizado en tiempo real. 
El chatbot de Streamlit tiene una caché inteligente configurada de **15 minutos** (`ttl=900` en el código). Esto significa que cualquier cambio que un administrador haga en la planilla de Google Sheets se reflejará de forma de actualización automática en el chatbot en un plazo máximo de 15 minutos, sin necesidad de reiniciar la app ni volver a desplegar el código. Esto previene sobrecargar el servidor con peticiones repetitivas.

### Si muevo el archivo de Google Sheets de carpeta, ¿se rompe el acceso?
**No.** Google Sheets identifica los archivos mediante una clave única contenida en el link (el ID largo entre `/d/` y `/pub`). Mover el archivo a otra carpeta de Google Drive o cambiarle el nombre no altera este ID, por lo que el acceso se mantendrá perfectamente y la app seguirá funcionando. Sólo se rompería si eliminas el archivo por completo o creas una copia nueva (ya que se generaría un nuevo ID).

---

## 📝 5. Configuración del Buzón de Sugerencias (Google Forms)

El chatbot cuenta con un formulario al pie de página para que los usuarios sugieran links que faltan. Si no configuras nada, las sugerencias se guardan localmente en tu servidor en un archivo llamado `sugerencias.csv`. 

Para enviarlas de forma automática a una planilla de Google Sheets:
1. Crea un **Google Form** con dos preguntas:
   * "Sucursal" (Texto corto o Selección)
   * "Trámite faltante" (Texto corto o Párrafo)
2. Abre el formulario en modo de edición, haz clic en los tres puntos de la esquina superior derecha y selecciona **"Obtener enlace rellenado previamente"** (Get pre-filled link).
3. Escribe cualquier respuesta de prueba y haz clic en **Obtener enlace**. Copia el enlace generado.
4. Ese enlace tendrá este formato:
   `https://docs.google.com/forms/d/e/1FAIpQLSc.../viewform?entry.1000001=Rosario&entry.1000002=Acuerdos`
   * Anota los códigos de entrada: en este caso `entry.1000001` y `entry.1000002` (estos identifican las preguntas).
5. Cambia el final de la URL del formulario de `/viewform` a `/formResponse`. Esa será tu URL de envío.
6. Agrega estas tres variables de entorno en los **Secrets de Streamlit Cloud**:
   ```toml
   GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/TU_FORM_ID/formResponse"
   GOOGLE_FORM_ENTRY_SUCURSAL = "entry.1000001"
   GOOGLE_FORM_ENTRY_TRAMITE = "entry.1000002"
   ```
Una vez configurado, cualquier sugerencia enviada desde el pie de página del chatbot se guardará directamente en tu Google Sheet vinculado al formulario.

---

## ✉️ 6. Derivación de Consultas y Registro Automático en Sheets

Si un usuario solicita un trámite o consulta algo que **no existe** en la base de datos de enlaces:
1. El asistente de Gemini identificará la ausencia del link.
2. Le responderá amablemente indicándole que no posee el enlace.
3. Generará automáticamente un botón interactivo llamado **"Derivar consulta a Administración Comercial"** (`mailto:`).
4. **REGISTRO EN SEGUNDO PLANO:** En ese mismo instante, la aplicación registrará **de forma automática** el trámite y la sucursal del usuario como una nueva sugerencia en el archivo `sugerencias.csv` (o en tu Google Sheet configurado en el paso 5). Los administradores verán esta entrada de inmediato sin que el usuario tenga que rellenar ningún formulario, lista para que escriban el URL y la activen.

---

## 💬 7. Notificaciones Automáticas a Google Chat

Para recibir una alerta instantánea en el canal de Google Chat de tu equipo cada vez que el chatbot no pueda responder una consulta (y así corregirlo rápidamente):

1. Ve a **Google Chat** y abre el Espacio (Space) de tu equipo de Administración Comercial.
2. Haz clic en el nombre del Espacio arriba y selecciona **Apps e integraciones** (Apps & Integrations).
3. Selecciona **Webhooks** y haz clic en **Agregar Webhook** (Add Webhook).
4. Escribe un nombre para el Bot (ej. *Asistente Operaciones*) y copia la URL generada.
5. Agrega esta variable a tus secretos de Streamlit Cloud (o en tu archivo `.streamlit/secrets.toml` local):
   ```toml
   GOOGLE_CHAT_WEBHOOK_URL = "URL_DE_TU_WEBHOOK_DE_GOOGLE_CHAT"
   ```

Una vez configurado, cada consulta no resuelta enviará una alerta automática formateada al canal de Chat indicando:
*   La sucursal del usuario.
*   El texto de la consulta que falló.
*   Una alerta llamando a la acción para agregar el link en la planilla.


