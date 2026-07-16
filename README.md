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
