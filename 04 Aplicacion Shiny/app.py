import matplotlib
matplotlib.use('Agg')

from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import os
from extractor import PDFExtractorEngine, TARGET_PERSONS
import logic
import providers

# --- ESTILADO CSS PREMIUM (Cyber-Noir & High-Fidelity Style) ---
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

/* --- Estilos Globales --- */
body {
    background-color: #0b090f;
    color: #e5e0eb;
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif;
    color: #ffffff;
    font-weight: 700;
}

/* Sidebar Custom Styling */
.sidebar {
    background-color: #0e0a17 !important;
    border-right: 1px solid rgba(168, 85, 247, 0.25) !important;
}

.control-label, 
label, 
.form-label, 
.form-check-label, 
.shiny-input-container label {
    color: #c084fc !important;
    font-weight: 700;
    margin-bottom: 0.4rem;
    font-size: 0.82rem;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

.form-control, 
select,
input[type="number"], 
input[type="text"], 
textarea {
    background-color: #161224 !important;
    color: #ffffff !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
    border-radius: 8px !important;
    padding: 0.45rem 0.6rem !important;
    font-size: 0.9rem;
}

.form-control:focus, 
select:focus,
input[type="number"]:focus,
textarea:focus {
    border-color: #d8b4fe !important;
    box-shadow: 0 0 8px rgba(216, 180, 254, 0.25) !important;
    outline: none !important;
}

.control-card {
    background: linear-gradient(135deg, rgba(26, 19, 44, 0.6) 0%, rgba(15, 10, 27, 0.85) 100%);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 14px;
    padding: 1.2rem 1.8rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    margin-bottom: 1.8rem;
}

.kpi-row {
    margin-bottom: 1.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.kpi-wrapper {
    flex: 1 1 15%;
    min-width: 145px;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(30, 22, 53, 0.5) 0%, rgba(15, 11, 27, 0.75) 100%);
    border: 1px solid rgba(168, 85, 247, 0.28);
    border-radius: 12px;
    padding: 0.9rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
    height: 100%;
}

.kpi-card:hover {
    border-color: #a855f7;
    background: rgba(168, 85, 247, 0.05);
}

.kpi-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #c084fc;
    margin-bottom: 0.2rem;
    font-weight: 600;
}

.kpi-value {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
}

/* Sephora Explanation Box Styling but Adapted to Forensic dark theme */
.explanation-box {
    background: rgba(15, 11, 27, 0.85);
    border-top: 1px solid rgba(168, 85, 247, 0.22);
    padding: 15px 20px;
    border-radius: 0 0 12px 12px;
    font-size: 0.86rem;
    color: #ebdff5;
    line-height: 1.6;
}

.explanation-title {
    font-weight: 700;
    color: #a855f7;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.88rem;
    letter-spacing: 0.5px;
}

/* Cards Premium */
.card {
    background-color: #120e1d !important;
    border: 1px solid rgba(168, 85, 247, 0.22) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    margin-bottom: 20px;
}

.card-header {
    background-color: rgba(168, 85, 247, 0.07) !important;
    border-bottom: 1px solid rgba(168, 85, 247, 0.22) !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 12px 20px !important;
}

.btn-primary {
    background: linear-gradient(135deg, #a855f7 0%, #701a75 100%) !important;
    border: 1px solid rgba(216, 180, 254, 0.4) !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3) !important;
    transition: all 0.2s ease !important;
}

.btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(168, 85, 247, 0.45) !important;
    border-color: #d8b4fe !important;
}

.btn-download {
    background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.25) !important;
}

.btn-download:hover {
    box-shadow: 0 6px 16px rgba(6, 182, 212, 0.35) !important;
    border-color: #22d3ee !important;
}

textarea.form-control {
    background-color: #0b0812 !important;
    color: #e2daf0 !important;
    font-family: 'Courier New', Courier, monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.45 !important;
    border: 1px solid rgba(168, 85, 247, 0.22) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    resize: none !important;
}

.meta-container {
    background: rgba(255, 255, 255, 0.012);
    border: 1px solid rgba(168, 85, 247, 0.15);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin-top: 0.8rem;
}

.meta-item-title {
    font-size: 0.75rem;
    color: #c084fc;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.meta-item-value {
    color: #ffffff;
    font-size: 0.85rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Tab Overrides */
.nav-tabs {
    border-bottom: 1px solid rgba(168, 85, 247, 0.25) !important;
    gap: 8px;
    margin-bottom: 20px;
}
.nav-link {
    color: #bfaec2 !important;
    border: 1px solid transparent !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}
.nav-link.active {
    background-color: rgba(168, 85, 247, 0.12) !important;
    border: 1px solid rgba(168, 85, 247, 0.35) !important;
    border-bottom: 1px solid #0b090f !important;
    color: #ffffff !important;
    box-shadow: 0 -4px 12px rgba(168, 85, 247, 0.08) !important;
}
.nav-link:hover:not(.active) {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(168, 85, 247, 0.15) !important;
}

/* Chat Styling */
.shiny-chat {
    flex-grow: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    min-height: 500px !important;
}

.shiny-chat-messages {
    flex-grow: 1 !important;
    overflow-y: auto !important;
    padding-bottom: 80px !important;
}

.chat-suggestion-box:hover {
    border-color: #a855f7 !important;
    background: rgba(168, 85, 247, 0.05) !important;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.15) !important;
    transform: translateY(-1px);
}

/* --- Eliminación Absoluta de la Barra Blanca Superior --- */
html, body, .container-fluid, main, .app-container {
    background-color: #0b090f !important;
    margin-top: 0 !important;
    padding-top: 0 !important;
    border-top: none !important;
}

header, .navbar, .app-header, .bslib-page-header, .bslib-navbar, .bslib-page-navbar {
    display: none !important;
}

.bslib-sidebar-layout {
    border: none !important;
    box-shadow: none !important;
}

/* --- Estilado Premium de Casillas de Selección (Checkboxes) --- */
.shiny-options-group {
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
    max-height: 250px !important;
    overflow-y: auto !important;
    padding-right: 8px !important;
    margin-bottom: 15px !important;
}

/* Scrollbar personalizada con estilo neón cyberpunk */
.shiny-options-group::-webkit-scrollbar {
    width: 6px !important;
}
.shiny-options-group::-webkit-scrollbar-track {
    background: rgba(25, 18, 44, 0.4) !important;
    border-radius: 4px !important;
}
.shiny-options-group::-webkit-scrollbar-thumb {
    background: rgba(168, 85, 247, 0.35) !important;
    border-radius: 4px !important;
    border: 1px solid rgba(168, 85, 247, 0.15) !important;
}
.shiny-options-group::-webkit-scrollbar-thumb:hover {
    background: rgba(168, 85, 247, 0.6) !important;
}

/* Contenedor del item checkbox */
.shiny-options-group .form-check {
    background: rgba(15, 10, 27, 0.85) !important;
    border: 1px solid rgba(168, 85, 247, 0.25) !important;
    border-radius: 8px !important;
    padding: 8px 12px 8px 32px !important;
    margin: 0 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    position: relative !important;
}

.shiny-options-group .form-check:hover {
    background: rgba(168, 85, 247, 0.08) !important;
    border-color: rgba(168, 85, 247, 0.5) !important;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.12) !important;
    transform: translateX(2px);
}

/* Checkbox circular/rounded neón */
.shiny-options-group .form-check-input {
    background-color: #161224 !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    width: 16px !important;
    height: 16px !important;
    border-radius: 4px !important;
    position: absolute !important;
    left: 10px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    margin: 0 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.shiny-options-group .form-check-input:checked {
    background-color: #a855f7 !important;
    border-color: #d8b4fe !important;
    box-shadow: 0 0 8px rgba(168, 85, 247, 0.6) !important;
}

.shiny-options-group .form-check-input:focus {
    box-shadow: 0 0 8px rgba(168, 85, 247, 0.4) !important;
    border-color: #a855f7 !important;
}

/* Etiqueta del checkbox */
.shiny-options-group .form-check-label {
    color: #e5e0eb !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0px !important;
    cursor: pointer !important;
    padding-left: 0 !important;
    user-select: none !important;
}

/* --- Estilo de Olvera AI Chat (Visibilidad de Letras) --- */
/* Forzar variables CSS heredables en los componentes web */
.shiny-chat, 
shiny-chat-messages,
.shiny-chat-messages,
.shiny-chat-message,
.message-body,
.message-content,
.markdown-container,
[id="chat"] {
    --chat-message-assistant-color: #e5e0eb !important;
    --chat-message-user-color: #ffffff !important;
    --chat-message-assistant-bg: rgba(168, 85, 247, 0.08) !important;
    --chat-message-user-bg: rgba(6, 182, 212, 0.08) !important;
    --bs-body-color: #e5e0eb !important;
    --bs-heading-color: #ffffff !important;
    color: #e5e0eb !important;
}

/* Reglas universales y de etiquetas específicas para penetrar selectores */
.shiny-chat *,
.shiny-chat p,
.shiny-chat li,
.shiny-chat span,
.shiny-chat div,
.shiny-chat strong,
.shiny-chat em,
.shiny-chat-messages *,
.shiny-chat-messages p,
.shiny-chat-messages li,
.shiny-chat-messages span,
.shiny-chat-messages div,
.shiny-chat-message-body *,
.shiny-chat-message-body p,
.shiny-chat-message-body li,
.shiny-chat-message-body span,
.message-body *,
.message-body p,
.message-body li,
.message-body span,
.message-content *,
.message-content p,
.message-content li,
.message-content span,
.markdown-container *,
.markdown-container p,
.markdown-container li,
.markdown-container span {
    color: #ebdff5 !important; /* Forzar el color lavanda legible en todo el contenido */
}

/* Habilitar colores especiales para resaltar títulos y negritas */
.shiny-chat strong,
.shiny-chat-messages strong,
.markdown-container strong,
.shiny-chat-message strong,
.shiny-chat-message-assistant strong,
.shiny-chat-message-user strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.shiny-chat h1, .shiny-chat h2, .shiny-chat h3, .shiny-chat h4,
.shiny-chat-messages h1, .shiny-chat-messages h2, .shiny-chat-messages h3,
.markdown-container h1, .markdown-container h2, .markdown-container h3,
.shiny-chat-message h1, .shiny-chat-message h2, .shiny-chat-message h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

/* Bordes y fondos de mensajes en el chat */
.shiny-chat-message-assistant,
shiny-chat-message[role="assistant"] {
    background-color: rgba(168, 85, 247, 0.08) !important;
    border: 1px solid rgba(168, 85, 247, 0.22) !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

.shiny-chat-message-user,
shiny-chat-message[role="user"] {
    background-color: rgba(6, 182, 212, 0.08) !important;
    border: 1px solid rgba(6, 182, 212, 0.22) !important;
    border-radius: 12px !important;
    padding: 12px !important;
}
"""

# Obtener lista de PDFs disponibles en la carpeta de datasets
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01 Datasets Usados"))
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
if not pdf_files:
    pdf_files = ["Ningún archivo en la carpeta de datasets"]

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.div(
            ui.h3("Proyecto Final: Analisis caso epstein", style="color: #ffffff; font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.95rem; letter-spacing: 1px; text-align: center; margin-top: 25px; border-bottom: 2px solid rgba(168, 85, 247, 0.35); padding-bottom: 15px; margin-bottom: 25px;"),
        ),
        
        ui.div(
            ui.p("💡 AUDITORÍA FORENSE:", style="font-weight: bold; color: #ffffff; font-size: 0.85em; letter-spacing: 0.5px;"),
            ui.p("Este sistema realiza minería de texto y análisis de co-ocurrencia sobre testimonios judiciales desclasificados. Emplea procesamiento de lenguaje natural y visualizaciones de grado de investigación para mapear redes de interés en el caso Epstein.", style="font-size: 0.82em; color: #ebdff5; line-height: 1.5;"),
            style="background: rgba(168, 85, 247, 0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(168, 85, 247, 0.2); margin-bottom: 20px;"
        ),
        
        # PANEL DE FILTROS INTERACTIVOS SEPHORA-STYLE
        ui.div(
            ui.div("🚨 FILTROS INTERACTIVOS", style="font-weight: 800; color: #a855f7; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 15px; text-transform: uppercase; border-left: 3px solid #a855f7; padding-left: 8px;"),
            
            # Filtro por Persona de Interés (Checkbox Group Sephora-Style)
            ui.input_checkbox_group(
                "selected_persons", 
                "Personas Clave:", 
                choices=TARGET_PERSONS, 
                selected=TARGET_PERSONS # Activar todas por defecto
            ),
            
            # Slider para Menciones Mínimas
            ui.input_slider(
                "min_mentions", 
                "Menciones Mínimas:", 
                min=1, 
                max=50, 
                value=1,
                step=1
            ),
            
            # Select para Radar de Tópicos
            ui.input_select(
                "dominant_topic", 
                "Resaltar Tópico:", 
                choices=["Todos", "Propiedades / Lugares", "Logística / Aviones", "Abuso / Menores", "Ámbito Legal / Juicio"], 
                selected="Todos"
            ),
            style="background: rgba(22, 18, 36, 0.7); border: 1px solid rgba(168, 85, 247, 0.25); padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.45); margin-bottom: 20px;"
        ),
        width=290,
        style="padding: 25px;"
    ),

    ui.div(
        # Rayas de Estilado Neon Purple y Dark (Stripes de Sephora adaptadas)
        ui.div(style="height: 6px; background: repeating-linear-gradient(90deg, #a855f7, #a855f7 15px, #0b090f 15px, #0b090f 30px); width: 100%; border-radius: 4px 4px 0 0; margin-bottom: 20px;"),
    ),

    ui.navset_tab(
        # TAB 1: Dashboard Forense
        ui.nav_panel(
            "Dashboard Forense",
            ui.div(
                ui.output_ui("forensic_dashboard_ui")
            )
        ),
        
        # TAB 2: Explorador de Transcripciones y Cronología
        ui.nav_panel(
            "Explorador de Transcripción",
            ui.div(
                ui.output_ui("document_explorer_ui")
            )
        ),
        
        # TAB 3: Olvera AI (AI Chatbot)
        ui.nav_panel(
            "Olvera AI",
            ui.div(
                ui.row(
                    ui.column(
                        12,
                        ui.div(
                            ui.output_ui("welcome_ui"),
                            style="margin-bottom: 20px;"
                        )
                    )
                ),
                ui.chat_ui("chat"),
                ui.output_ui("chat_toolbar_ui"),
                style="padding: 20px; max-width: 900px; margin: 0 auto;"
            )
        ),
        id="main_nav_tabs"
    ),
    
    ui.tags.head(
        ui.tags.style(CUSTOM_CSS)
    ),
    title=""
)


# --- LÓGICA DEL SERVIDOR (SERVER) ---
def server(input, output, session):
    
    is_empty = reactive.Value(True)
    chat = ui.Chat(id="chat")

    # Obtener el motor de procesamiento para el archivo seleccionado
    @reactive.calc
    def pdf_engine():
        if not pdf_files or pdf_files[0].startswith("Ningún archivo"):
            return None
        
        datapath = os.path.join(DATA_DIR, pdf_files[0])
        if not os.path.exists(datapath):
            return None
            
        return PDFExtractorEngine(datapath)

    # Reactive calc para el total de páginas del PDF cargado
    @reactive.calc
    def pdf_pages():
        engine = pdf_engine()
        return engine.num_pages if engine else 1

    # Proceso de extracción e inteligencia forense reactiva
    @reactive.calc
    def extraction_results():
        engine = pdf_engine()
        
        # Si no hay PDF, usar engine en modo CSV-only (lee los datasets precalculados directamente)
        if not engine:
            engine = PDFExtractorEngine(None)
        
        start = 1
        # Si el engine no tiene PDF cargado, usar el total conocido del corpus (5,028 páginas)
        end = engine.num_pages if engine.num_pages > 0 else 5028
        clean = True
        lang = "en"
            
        text, metrics = engine.process_document(start, end, clean=clean, language=lang)
        
        orig_name = pdf_files[0] if pdf_files and not pdf_files[0].startswith("Ningún") else "Epstein_documents.pdf"
        filename = f"forensic_{orig_name.replace('.pdf', '')}.txt"
        meta = engine.extract_metadata()
        
        return {
            "text": text,
            "metrics": metrics,
            "filename": filename,
            "metadata": meta,
            "pages_processed": end
        }


    # Descargar TXT limpio
    @render.download(filename=lambda: extraction_results()["filename"] if extraction_results() else "forensic.txt")
    def download_btn():
        results = extraction_results()
        if not results:
            return None
        path = "temp_extracted.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(results["text"])
        return path

    # RENDERIZADO DEL TAB 1: DASHBOARD FORENSE
    @render.ui
    def forensic_dashboard_ui():
        try:
            results = extraction_results()
        except Exception:
            results = None
            
        if not results:
            return ui.div(
                ui.span("⚠️", style="font-size: 3.5rem; display: block; margin-bottom: 0.8rem;"),
                ui.h4("Error de Carga o Inicialización", style="color: #ef4444;"),
                ui.p("Por favor, asegúrate de que el archivo Epstein_documents.pdf exista en la carpeta '01 Datasets Usados'.", style="color: #bfaec2;"),
                style="text-align: center; padding: 5rem 2rem; background: rgba(255,255,255,0.012); border-radius: 12px; border: 1px dashed rgba(239,68,68,0.2);"
            )
            
        metrics = results["metrics"]
        
        return ui.div(
            # Fila de KPIs
            ui.div(
                ui.div(
                    ui.div(
                        ui.div("Páginas Escaneadas", class_="kpi-title"),
                        ui.div(f"{results['pages_processed']}", class_="kpi-value", style="color: #c084fc;"),
                        class_="kpi-card"
                    ),
                    class_="kpi-wrapper"
                ),
                ui.div(
                    ui.div(
                        ui.div("Palabras Procesadas", class_="kpi-title"),
                        ui.div(f"{metrics['total_words']:,}", class_="kpi-value"),
                        class_="kpi-card"
                    ),
                    class_="kpi-wrapper"
                ),
                ui.div(
                    ui.div(
                        ui.div("Menciones Censuradas", class_="kpi-title"),
                        ui.div(f"🔏 {metrics['redactions_count']:,}", class_="kpi-value", style="color: #ef4444;"),
                        class_="kpi-card"
                    ),
                    class_="kpi-wrapper"
                ),
                ui.div(
                    ui.div(
                        ui.div("Índice Censura (x1k)", class_="kpi-title"),
                        ui.div(f"{metrics['censorship_index']:.1f}", class_="kpi-value", style="color: #fca5a5;"),
                        class_="kpi-card"
                    ),
                    class_="kpi-wrapper"
                ),
                ui.div(
                    ui.div(
                        ui.div("Total Evasivas", class_="kpi-title"),
                        ui.div(f"🤐 {metrics['evasions_count']:,}", class_="kpi-value", style="color: #eab308;"),
                        class_="kpi-card"
                    ),
                    class_="kpi-wrapper"
                ),
                ui.div(
                    ui.div(
                        ui.div("Índice Evasividad (x1k)", class_="kpi-title"),
                        ui.div(f"{metrics['evasiveness_index']:.1f}", class_="kpi-value", style="color: #fef08a;"),
                        class_="kpi-card"
                    ),
                    class_="kpi-wrapper"
                ),
                class_="kpi-row"
            ),
            
            ui.hr(style="border-color: rgba(168, 85, 247, 0.2); margin: 1.2rem 0;"),
            
            # FILA DE GRÁFICOS 1 (Top 10 Personas y Co-ocurrencias)
            ui.layout_columns(
                ui.card(
                    ui.card_header("Personas Clave Identificadas (Menciones)"),
                    ui.output_plot("person_chart"),
                    ui.div(
                        ui.div("👥 ANÁLISIS DE ENTIDADES DE ALTO INTERÉS", class_="explanation-title"),
                        ui.p("Rastrea menciones de personajes clave en la red del caso Epstein (como Ghislaine Maxwell, Donald Trump, Virginia Giuffre, Prince Andrew, Bill Clinton) combinando listas y heurísticas de reconocimiento de entidades."),
                        class_="explanation-box"
                    )
                ),
                ui.card(
                    ui.card_header("Red de Co-ocurrencia Social en Páginas"),
                    ui.output_plot("co_occur_chart"),
                    ui.div(
                        ui.div("🕸️ MAPA DE RELACIONES FORENSES", class_="explanation-title"),
                        ui.p("Identifica qué personas de interés aparecen juntas en la misma página del documento. Esencial para destapar conexiones directas, reuniones o menciones cruzadas en los testimonios."),
                        class_="explanation-box"
                    )
                ),
                col_widths=[7, 5]
            ),
            
            # FILA DE GRÁFICOS 2 (Evasión Verbal y Temáticas)
            ui.layout_columns(
                ui.card(
                    ui.card_header("Tácticas de Evasividad Verbal Detectadas"),
                    ui.output_plot("evasions_details_chart"),
                    ui.div(
                        ui.div("🤐 PERFIL DE POSTURA DEFENSIVA", class_="explanation-title"),
                        ui.p("Clasifica las evasiones lingüísticas más comunes realizadas en el documento, distinguiendo objeciones de abogados de la pérdida de memoria alegada ('no recuerdo') o apelaciones constitucionales a la Quinta Enmienda."),
                        class_="explanation-box"
                    )
                ),
                ui.card(
                    ui.card_header("Prevalencia Temática en el Documento"),
                    ui.output_plot("topics_prevalence_chart"),
                    ui.div(
                        ui.div("🚩 MAPEO DE TEMÁTICAS DE SOSPECHA", class_="explanation-title"),
                        ui.p("Cuantifica el volumen de palabras asociadas a categorías sospechosas: Propiedades/Lugares de interés, Logística y vuelos de Lolita Express, Tópicos de Abuso y vocabulario del Ámbito Judicial del Juicio."),
                        class_="explanation-box"
                    )
                ),
                col_widths=[6, 6]
            ),
            
            ui.hr(style="border-color: rgba(168, 85, 247, 0.2); margin: 1.2rem 0;"),
            
            # FILA DE GRÁFICOS 3 (Riesgo vs Sentimiento y Vocabulario Clave)
            ui.layout_columns(
                ui.card(
                    ui.card_header("Correlación de Riesgo vs Sentimiento por Persona"),
                    ui.output_plot("risk_sentiment_chart"),
                    ui.div(
                        ui.div("⚠️ CUADRANTE DE RIESGO SEMÁNTICO", class_="explanation-title"),
                        ui.p("Cruza el Índice de Sentimiento Forense (eje X, negativo a positivo) con el Índice de Riesgo Forense (eje Y, co-ocurrencia con abusos o logística). Las burbujas más grandes indican mayor volumen de menciones. Los implicados en el cuadrante superior izquierdo representan el perfil de mayor criticidad en el expediente."),
                        class_="explanation-box"
                    )
                ),
                ui.card(
                    ui.card_header("Top 10 Vocablos Semánticos más Frecuentes"),
                    ui.output_plot("content_words_chart"),
                    ui.div(
                        ui.div("📝 ANÁLISIS DE FRECUENCIA DE TÉRMINOS", class_="explanation-title"),
                        ui.p("Muestra los términos generales más recurrentes dentro de la transcripción judicial, excluyendo stopwords y nombres propios. Revela los conceptos clave en torno a los cuales giran las deposiciones y testimonios."),
                        class_="explanation-box"
                    )
                ),
                col_widths=[6, 6]
            )
        )

    # RENDERIZADO DEL TAB 2: EXPLORADOR DE DOCUMENTOS Y CRONOLOGÍA
    @render.ui
    def document_explorer_ui():
        try:
            results = extraction_results()
        except Exception:
            results = None
            
        if not results:
            return ui.div(
                ui.span("⚠️", style="font-size: 3.5rem; display: block; margin-bottom: 0.8rem;"),
                ui.h4("Error de Carga o Inicialización", style="color: #ef4444;"),
                ui.p("Por favor, asegúrate de que el archivo Epstein_documents.pdf exista en la carpeta '01 Datasets Usados'.", style="color: #bfaec2;"),
                style="text-align: center; padding: 5rem 2rem; background: rgba(255,255,255,0.012); border-radius: 12px; border: 1px dashed rgba(239,68,68,0.2);"
            )
            
        meta = results["metadata"]
        title_val = meta.get("Título", "No especificado")
        author_val = meta.get("Autor", "No especificado")
        
        return ui.layout_columns(
            ui.card(
                ui.card_header("⚖️ Vista Previa Judicial (Transcripción Limpia)"),
                ui.input_text_area(
                    "preview_area", 
                    "", 
                    value=results["text"][:3500] + ("\n\n[Expediente truncado para visualización rápida...]" if len(results["text"]) > 3500 else ""), 
                    height="320px", 
                    width="100%"
                ),
                ui.download_button(
                    "download_btn", 
                    "📥 DESCARGAR TRANSCRIPCIÓN FORENSE (.TXT)", 
                    class_="btn-primary btn-download w-100",
                    style="margin-top: 0.8rem;"
                ),
                ui.div(
                    ui.row(
                        ui.column(6, ui.div(ui.div("Título de Expediente", class_="meta-item-title"), ui.div(title_val, class_="meta-item-value"))),
                        ui.column(6, ui.div(ui.div("Autoría Legal", class_="meta-item-title"), ui.div(author_val, class_="meta-item-value")))
                    ),
                    class_="meta-container"
                )
            ),
            ui.card(
                ui.card_header("📅 Frecuencia Temporal (Años Mencionados)"),
                ui.output_plot("timeline_chart"),
                ui.div(
                    ui.div("📅 HISTOGRAMA CRONOLÓGICO FORENSE", class_="explanation-title"),
                    ui.p("Rastrea la presencia de años lógicos específicos dentro de los testimonios o deposiciones judiciales. Ayuda a identificar en qué años se concentran los abusos o vuelos reportados en este expediente judicial."),
                    class_="explanation-box"
                )
            ),
            col_widths=[8, 4]
        )

    # --- MATPLOTLIB PLOTS ---
    
    @render.plot
    def person_chart():
        results = extraction_results()
        if not results or not results["metrics"]["top_persons"]:
            fig, ax = plt.subplots(figsize=(5, 3.8), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.axis('off')
            return fig
            
        top_persons = results["metrics"]["top_persons"]
        selected = list(input.selected_persons())
        min_m = input.min_mentions()
        filtered = [item for item in top_persons if item[0] in selected and item[1] >= min_m]
        
        if not filtered:
            fig, ax = plt.subplots(figsize=(5, 3.8), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.text(0.5, 0.5, "Sin resultados para los filtros seleccionados", ha='center', va='center', color='#bfaec2', fontsize=9)
            ax.axis('off')
            return fig
            
        names = [item[0] for item in filtered][::-1] 
        freqs = [item[1] for item in filtered][::-1]
        
        fig, ax = plt.subplots(figsize=(5, 3.8), facecolor='#0b090f')
        ax.set_facecolor('#0b090f')
        
        bars = ax.barh(names, freqs, color='#a855f7', edgecolor='#d8b4fe', height=0.55)
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.xaxis.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax.set_axisbelow(True)
        ax.tick_params(colors='#bfaec2', labelsize=9, length=0)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + (max(freqs)*0.015 if max(freqs)>0 else 0), 
                bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', 
                ha='left', 
                va='center', 
                color='#d8b4fe', 
                fontweight='bold', 
                fontsize=8.5
            )
        plt.tight_layout()
        return fig

    @render.ui
    def person_list_ui():
        results = extraction_results()
        if not results or not results["metrics"]["top_persons"]:
            return None
            
        top_persons = results["metrics"]["top_persons"]
        selected = list(input.selected_persons())
        min_m = input.min_mentions()
        filtered = [item for item in top_persons if item[0] in selected and item[1] >= min_m]
        
        if not filtered:
            return ui.p("Sin personas bajo los filtros seleccionados.", style="color: #bfaec2; font-style: italic; font-size: 0.85rem;")
            
        list_items = []
        for i, (name, freq) in enumerate(filtered, 1):
            emoji = "🚨" if i == 1 else "📌" if i <= 3 else "▪"
            list_items.append(
                ui.div(
                    ui.span(f"{emoji} {i}. "),
                    ui.strong(f"{name}", style="color: #ffffff;"),
                    ui.span(f" ({freq} menciones)"),
                    style="margin-bottom: 0.3rem; font-size: 0.9rem;"
                )
            )
        return ui.div(*list_items)

    @render.plot
    def co_occur_chart():
        results = extraction_results()
        if not results or not results["metrics"].get("top_co_occurrences"):
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.text(0.5, 0.5, "Sin co-ocurrencias suficientes", ha='center', va='center', color='#bfaec2', fontsize=10)
            ax.axis('off')
            return fig
            
        top_co = results["metrics"]["top_co_occurrences"]
        selected = list(input.selected_persons())
        filtered = []
        for pair, freq in top_co:
            parts = pair.split(" & ")
            if len(parts) == 2 and parts[0] in selected and parts[1] in selected:
                filtered.append((pair, freq))
                
        if not filtered:
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.text(0.5, 0.5, "Sin conexiones para los filtros activos", ha='center', va='center', color='#bfaec2', fontsize=9)
            ax.axis('off')
            return fig
            
        pairs = [item[0] for item in filtered][::-1] 
        freqs = [item[1] for item in filtered][::-1]
        
        fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
        ax.set_facecolor('#0b090f')
        
        bars = ax.barh(pairs, freqs, color='#06b6d4', edgecolor='#22d3ee', height=0.55)
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.xaxis.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax.set_axisbelow(True)
        ax.tick_params(colors='#bfaec2', labelsize=8.5, length=0)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + (max(freqs)*0.015 if max(freqs)>0 else 0), 
                bar.get_y() + bar.get_height()/2, 
                f'{int(width)} pág', 
                ha='left', 
                va='center', 
                color='#22d3ee', 
                fontweight='bold', 
                fontsize=8.5
            )
        plt.tight_layout()
        return fig

    @render.plot
    def timeline_chart():
        results = extraction_results()
        if not results or not results["metrics"].get("timeline"):
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.axis('off')
            return fig
            
        timeline = results["metrics"]["timeline"]
        timeline_filtered = [item for item in timeline if 1995 <= int(item[0]) <= 2024]
        if not timeline_filtered:
            timeline_filtered = timeline
            
        years = [int(item[0]) for item in timeline_filtered]
        freqs = [item[1] for item in timeline_filtered]
        
        fig, ax = plt.subplots(figsize=(6, 3.2), facecolor='#0b090f')
        ax.set_facecolor('#0b090f')
        
        ax.plot(years, freqs, color='#f43f5e', linewidth=2.2, marker='o', markersize=5, markerfacecolor='#ffffff', markeredgecolor='#f43f5e')
        ax.fill_between(years, freqs, color='#f43f5e', alpha=0.15)
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.yaxis.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax.xaxis.grid(True, linestyle='--', alpha=0.05, color='#ffffff')
        ax.set_axisbelow(True)
        ax.tick_params(colors='#bfaec2', labelsize=8.5, length=0)
        
        import matplotlib.ticker as ticker
        ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    @render.plot
    def evasions_details_chart():
        results = extraction_results()
        if not results or "evasions_details" not in results["metrics"]:
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.axis('off')
            return fig
            
        details = results["metrics"]["evasions_details"]
        labels = list(details.keys())
        sizes = list(details.values())
        
        if sum(sizes) == 0:
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.text(0.5, 0.5, "Sin tácticas de evasión detectadas", ha='center', va='center', color='#bfaec2', fontsize=10)
            ax.axis('off')
            return fig
            
        colors = ['#eab308', '#ca8a04', '#a16207', '#854d0e', '#713f12']
        
        fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
        ax.set_facecolor('#0b090f')
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors, 
            autopct='%1.1f%%', 
            startangle=140, 
            pctdistance=0.75,
            textprops=dict(color='#bfaec2', size=8.5),
            wedgeprops=dict(width=0.45, edgecolor='#0b090f', linewidth=2)
        )
        
        for autotext in autotexts:
            autotext.set_color('#ffffff')
            autotext.set_fontsize(8.5)
            autotext.set_weight('bold')
            
        ax.axis('equal')  
        plt.tight_layout()
        return fig

    @render.plot
    def topics_prevalence_chart():
        results = extraction_results()
        if not results or "topic_scores" not in results["metrics"]:
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.axis('off')
            return fig
            
        scores = results["metrics"]["topic_scores"]
        topics = list(scores.keys())
        values = list(scores.values())
        
        fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
        ax.set_facecolor('#0b090f')
        
        # Determinar colores reactivos basados en el filtro de Sephora
        colors = []
        edgecolors = []
        selected_topic = input.dominant_topic()
        for t in topics:
            if selected_topic != "Todos" and t.startswith(selected_topic[:5]):
                colors.append('#f43f5e') # Rosa neón Sephora
                edgecolors.append('#ffffff') # Resaltado blanco pulido
            else:
                colors.append('#10b981') # Verde esmeralda por defecto
                edgecolors.append('#34d399')
        
        bars = ax.bar(topics, values, color=colors, edgecolor=edgecolors, width=0.45)
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.yaxis.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax.set_axisbelow(True)
        ax.tick_params(colors='#bfaec2', labelsize=8.5, length=0)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            is_highlighted = (selected_topic != "Todos" and topics[i].startswith(selected_topic[:5]))
            ax.text(
                bar.get_x() + bar.get_width()/2, 
                height + (max(values)*0.015 if max(values)>0 else 0), 
                f'{int(height)}', 
                ha='center', 
                va='bottom', 
                color='#ffffff' if is_highlighted else '#34d399', 
                fontweight='bold', 
                fontsize=8.5
            )
        plt.tight_layout()
        return fig

    @render.plot
    def risk_sentiment_chart():
        results = extraction_results()
        if not results or not results["metrics"].get("person_sentiment_analytics"):
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.axis('off')
            return fig
            
        analytics = results["metrics"]["person_sentiment_analytics"]
        selected = list(input.selected_persons())
        min_m = input.min_mentions()
        valid_data = [p for p in analytics if p["Persona"] in selected and p["Menciones"] >= min_m]
        
        if not valid_data:
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.text(0.5, 0.5, "Sin correlaciones para los filtros activos", ha='center', va='center', color='#bfaec2', fontsize=9)
            ax.axis('off')
            return fig
            
        names = [p["Persona"] for p in valid_data]
        sentiment = [p["Indice Sentimiento"] for p in valid_data]
        risk = [p["Indice de Riesgo Forense"] for p in valid_data]
        mentions = [p["Menciones"] for p in valid_data]
        
        fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
        ax.set_facecolor('#0b090f')
        
        max_mentions = max(mentions) if mentions else 1
        sizes = [max(80, (m / max_mentions) * 450) for m in mentions]
        
        scatter = ax.scatter(sentiment, risk, s=sizes, c=risk, cmap='plasma', alpha=0.75, edgecolors='#ffffff', linewidths=1)
        
        for i, txt in enumerate(names):
            ax.annotate(
                txt, 
                (sentiment[i], risk[i]),
                xytext=(5, 5), 
                textcoords='offset points',
                color='#ffffff',
                fontsize=7.8,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', fc='black', alpha=0.4, ec='none')
            )
            
        for spine in ax.spines.values():
            spine.set_color((168/255, 85/255, 247/255, 0.2))
            
        ax.xaxis.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax.yaxis.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax.set_axisbelow(True)
        
        ax.tick_params(colors='#bfaec2', labelsize=8.5)
        ax.set_xlim(-1.05, 1.05)
        
        ax.axvline(0, color=(1.0, 1.0, 1.0, 0.15), linestyle=':', linewidth=1)
        ax.axhline(sum(risk)/len(risk) if risk else 1, color=(1.0, 1.0, 1.0, 0.15), linestyle=':', linewidth=1)
        
        plt.tight_layout()
        return fig

    @render.plot
    def content_words_chart():
        results = extraction_results()
        if not results or not results["metrics"].get("top_words"):
            fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
            ax.set_facecolor('#0b090f')
            ax.axis('off')
            return fig
            
        top_words = results["metrics"]["top_words"]
        words = [item[0] for item in top_words][::-1]
        freqs = [item[1] for item in top_words][::-1]
        
        fig, ax = plt.subplots(figsize=(5, 3.2), facecolor='#0b090f')
        ax.set_facecolor('#0b090f')
        
        bars = ax.barh(words, freqs, color='#f59e0b', edgecolor='#fcd34d', height=0.55)
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.xaxis.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax.set_axisbelow(True)
        ax.tick_params(colors='#bfaec2', labelsize=9, length=0)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + (max(freqs)*0.015 if max(freqs)>0 else 0), 
                bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', 
                ha='left', 
                va='center', 
                color='#fcd34d', 
                fontweight='bold', 
                fontsize=8.5
            )
        plt.tight_layout()
        return fig


    #     @chat.on_user_submit
    async def _handle_user_submit():
        is_empty.set(False)
        ui_messages = list(chat.messages())
        if len(ui_messages) > 10:
            ui_messages = ui_messages[-10:]
            
        # Crear copia limpia para enviar al LLM y evitar inyectar 10k caracteres en el globo de la UI
        llm_messages = []
        for m in ui_messages:
            role = m.role if hasattr(m, 'role') else m.get('role', '')
            content = m.content if hasattr(m, 'content') else m.get('content', '')
            llm_messages.append({"role": role, "content": content})
            
        # Inyectar el contexto de la transcripción y métricas forenses al mensaje enviado a la IA
        try:
            with reactive.isolate():
                results = extraction_results()
            if results:
                metrics = results["metrics"]
                meta = results["metadata"]
                
                doc_name = pdf_files[0] if pdf_files else "Epstein_documents.pdf"
                ctx = f"\n\n[CONTEXTO DE ANÁLISIS FORENSE - DOCUMENTO: {doc_name}]\n"
                ctx += f"Páginas escaneadas: {results['pages_processed']} (Documento Completo)\n"
                ctx += f"Menciones de Censura [REDACTED]: {metrics['redactions_count']} (Índice: {metrics['censorship_index']:.1f})\n"
                ctx += f"Total de Evasiones Verbales: {metrics['evasiones_count']} (Índice: {metrics['evasiveness_index']:.1f})\n"
                ctx += f"Prevalencia Temática: {metrics['topic_scores']}\n"
                ctx += f"Metadatos del PDF: {meta}\n"
                ctx += f"Fragmento del expediente: {results['text'][:10000]} (fin del fragmento)\n"
                
                if llm_messages and llm_messages[-1]["role"] == "user":
                    llm_messages[-1]["content"] += ctx
        except Exception as e:
            print(f"Error inyectando contexto forense al Copilot: {e}")

        async_gen = logic.stream_chat_response(
            messages=llm_messages,
            model=providers.DEFAULT_MODEL,
            web_search_enabled=False,
            image_b64=None
        )
        await chat.append_message_stream(async_gen)

    # Evento de click en sugerencia de chat
    @reactive.Effect
    @reactive.event(input.suggestion_click)
    async def _handle_suggestion():
        prompt = input.suggestion_click()
        if not prompt:
            return
        is_empty.set(False)
        await chat.append_message({"role": "user", "content": prompt})
        
        # Enviar inmediatamente con el contexto inyectado
        try:
            with reactive.isolate():
                results = extraction_results()
            if results:
                metrics = results["metrics"]
                meta = results["metadata"]
                
                doc_name = pdf_files[0] if pdf_files else "Epstein_documents.pdf"
                ctx = f"\n\n[CONTEXTO DE ANÁLISIS FORENSE - DOCUMENTO: {doc_name}]\n"
                ctx += f"Páginas escaneadas: {results['pages_processed']} (Documento Completo)\n"
                ctx += f"Menciones de Censura [REDACTED]: {metrics['redactions_count']} (Índice: {metrics['censorship_index']:.1f})\n"
                ctx += f"Total de Evasiones Verbales: {metrics['evasions_count']} (Índice: {metrics['evasiveness_index']:.1f})\n"
                ctx += f"Prevalencia Temática: {metrics['topic_scores']}\n"
                ctx += f"Metadatos del PDF: {meta}\n"
                ctx += f"Fragmento del expediente: {results['text'][:10000]} (fin del fragmento)\n"
                
                enriched_prompt = prompt + ctx
            else:
                enriched_prompt = prompt
        except Exception as e:
            print(f"Error inyectando contexto de sugerencia forense: {e}")
            enriched_prompt = prompt
            
        messages = [{"role": "user", "content": enriched_prompt}]
        async_gen = logic.stream_chat_response(
            messages=messages,
            model=providers.DEFAULT_MODEL,
            web_search_enabled=False,
            image_b64=None
        )
        await chat.append_message_stream(async_gen)

    @output
    @render.ui
    def welcome_ui():
        if not is_empty.get():
            return ui.div()
        return ui.div(
            ui.div(
                ui.HTML("""
                    <div style="width:68px;height:68px;background:#161224;border:1px solid #a855f7;border-radius:18px;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;box-shadow:0 10px 30px rgba(168,85,247,0.2)">
                        <svg viewBox='0 0 24 24' fill='none' stroke='#c084fc' stroke-width='1.5' style='width:38px;height:38px;'>
                            <path d='M12 2L3 7V17L12 22L21 17V7L12 2Z'/>
                            <path d='M12 22V12'/><path d='M12 12L21 7'/><path d='M12 12L3 7'/>
                        </svg>
                    </div>
                    <h2 style='font-family:"Space Grotesk",sans-serif;font-weight:800;font-size:1.4rem;color:#ffffff;margin-bottom:8px;'>Hola, soy Olvera AI</h2>
                    <p style='color:#bfaec2;font-size:0.95rem;'>Tengo acceso en tiempo real a los resultados de minería y transcripciones forenses del documento. ¿Qué deseas examinar?</p>
                """),
                style="text-align:center;padding:30px 20px 20px;"
            ),
            ui.div(
                ui.div(
                    ui.HTML("<div style='font-weight:700;color:#ffffff;font-size:0.9rem;margin-bottom:4px;'>📊 Explicar Métricas</div><div style='color:#bfaec2;font-size:0.82rem;'>Analiza los gráficos y los KPIs actuales</div>"),
                    onclick="Shiny.setInputValue('suggestion_click', 'Analiza y resume los KPIs y gráficos forenses del documento actual', {priority:'event'})",
                    class_="chat-suggestion-box",
                    style="background:#161224;border:1px solid rgba(168,85,247,0.22);border-radius:10px;padding:14px 16px;cursor:pointer;transition:all 0.2s;"
                ),
                ui.div(
                    ui.HTML("<div style='font-weight:700;color:#ffffff;font-size:0.9rem;margin-bottom:4px;'>👥 Personas Implicadas</div><div style='color:#bfaec2;font-size:0.82rem;'>Busca conexiones e implicaciones de red</div>"),
                    onclick="Shiny.setInputValue('suggestion_click', '¿Qué personas clave tienen mayor número de menciones y co-ocurrencias en este expediente y qué sugiere esto?', {priority:'event'})",
                    class_="chat-suggestion-box",
                    style="background:#161224;border:1px solid rgba(168,85,247,0.22);border-radius:10px;padding:14px 16px;cursor:pointer;transition:all 0.2s;"
                ),
                ui.div(
                    ui.HTML("<div style='font-weight:700;color:#ffffff;font-size:0.9rem;margin-bottom:4px;'>🤐 Estrategia de Evasión</div><div style='color:#bfaec2;font-size:0.82rem;'>Analiza las tácticas evasivas del testimonio</div>"),
                    onclick="Shiny.setInputValue('suggestion_click', 'Evalúa las tácticas de evasión verbal encontradas. ¿Se observa una postura defensiva o evasiva sistemática?', {priority:'event'})",
                    class_="chat-suggestion-box",
                    style="background:#161224;border:1px solid rgba(168,85,247,0.22);border-radius:10px;padding:14px 16px;cursor:pointer;transition:all 0.2s;"
                ),
                ui.div(
                    ui.HTML("<div style='font-weight:700;color:#ffffff;font-size:0.9rem;margin-bottom:4px;'>🔏 Censura e Información</div><div style='color:#bfaec2;font-size:0.82rem;'>Determina el nivel de censura [REDACTED]</div>"),
                    onclick="Shiny.setInputValue('suggestion_click', 'Explica el índice de censura encontrado. ¿Qué tan censurado está el documento y qué podemos deducir?', {priority:'event'})",
                    class_="chat-suggestion-box",
                    style="background:#161224;border:1px solid rgba(168,85,247,0.22);border-radius:10px;padding:14px 16px;cursor:pointer;transition:all 0.2s;"
                ),
                style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 20px 20px;"
            ),
            style="max-width:680px;margin:0 auto;"
        )

    @output
    @render.ui
    def chat_toolbar_ui():
        return ui.HTML("""
            <div style='border-top:1px solid rgba(168, 85, 247, 0.2);padding:12px 10px 0;margin-top:8px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;'>
                <span style='font-size:0.78rem;color:#ffffff;font-weight:700;letter-spacing:0.5px;'>OLVERA AI</span>
                <span style='font-size:0.78rem;color:rgba(168,85,247,0.4);'>|</span>
                <span style='font-size:0.78rem;color:#bfaec2;'>Gemini 3 Flash &bull; Contexto completo de transcripción y KPIs inyectados reactivamente</span>
            </div>
        """)

# Instanciar aplicación Shiny
app = App(app_ui, server)
