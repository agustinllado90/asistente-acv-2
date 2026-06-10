import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Asistente ACV",
    page_icon="🧠",
    layout="centered"
)

# 2. FUNCIÓN PARA RENDERIZAR LAS IMÁGENES DE REFERENCIA
def render_reference_images(stage_data):
    """
    stage_data: lista de dicts con info de cada secuencia
    Ejemplo:
    [
      {"seq": "DWI", "label": "Hiperintensa", "brain_bg": "#1A1A1A", "lesion_color": "#F5F5F5", "label_color": "#F5F5F5"},
      ...
    ]
    """
    cards_html = ""
    for s in stage_data:
        # El "cerebro" simulado: fondo de tejido cerebral + mancha de lesión
        brain_bg = s["brain_bg"]        # color del parénquima normal
        lesion_c = s["lesion_color"]    # color de la lesión
        lesion_opacity = s.get("lesion_opacity", "1")
        extra_note = s.get("note", "")

        cards_html += f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 130px;
        ">
          <!-- Simulación de corte axial cerebral -->
          <div style="
            width: 110px;
            height: 110px;
            border-radius: 50%;
            background: {brain_bg};
            border: 2px solid #444;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.4);
          ">
            <!-- Lesión: mancha oval en el hemisferio izquierdo -->
            <div style="
              position: absolute;
              top: 22px;
              left: 20px;
              width: 38px;
              height: 32px;
              border-radius: 50%;
              background: {lesion_c};
              opacity: {lesion_opacity};
              border: 1.5px solid rgba(200,200,200,0.3);
            "></div>
            <!-- Surcos cerebrales decorativos -->
            <div style="
              position: absolute;
              width: 80px;
              height: 1px;
              background: rgba(150,150,150,0.3);
              top: 50%;
            "></div>
            <div style="
              position: absolute;
              width: 1px;
              height: 80px;
              background: rgba(150,150,150,0.3);
              left: 50%;
            "></div>
          </div>
          <!-- Etiqueta de secuencia -->
          <div style="
            margin-top: 6px;
            font-weight: bold;
            font-size: 13px;
            color: #E0E0E0;
            font-family: monospace;
          ">{s['seq']}</div>
          <!-- Descripción de señal -->
          <div style="
            margin-top: 3px;
            font-size: 11px;
            color: {s['label_color']};
            text-align: center;
            font-family: sans-serif;
            line-height: 1.3;
          ">{s['label']}</div>
          {f'<div style="font-size: 10px; color: #AAAAAA; text-align: center; margin-top: 2px;">{extra_note}</div>' if extra_note else ''}
        </div>
        """

    full_html = f"""
    <div style="
        background: #1A1A2E;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 16px 10px 12px 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    ">
      <div style="
        font-size: 12px;
        color: #AAAAAA;
        font-family: sans-serif;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 4px;
      ">Patrón de señal esperado</div>
      <div style="
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        justify-content: center;
        max-width: 290px;
        margin: 0 auto;
      ">
        {cards_html}
      </div>
      <div style="font-size: 10px; color: #666; font-family: sans-serif; margin-top: 4px;">
        ● Representación esquemática — no reemplaza imágenes reales
      </div>
    </div>
    """
    # Altura dinámica: las tarjetas se acomodan en una grilla de 2 columnas,
    # así que reservamos espacio según la cantidad de filas (2 tarjetas por fila).
    filas = (len(stage_data) + 1) // 2
    altura = 120 + filas * 175
    components.html(full_html, height=altura, scrolling=False)


# PALETA DE COLORES POR INTENSIDAD DE SEÑAL
HIPER    = {"brain_bg": "#1A1A1A", "lesion_color": "#F5F5F5", "label_color": "#F5F5F5"}  # tejido oscuro, lesión blanca
ISO      = {"brain_bg": "#555555", "lesion_color": "#555555", "label_color": "#AAAAAA"}   # todo igual, no se distingue
HIPO     = {"brain_bg": "#AAAAAA", "lesion_color": "#1A1A1A", "label_color": "#888888"}   # tejido gris, lesión negra
LEV_HIPO = {"brain_bg": "#888888", "lesion_color": "#2A2A2A", "label_color": "#999999"}
LEV_HIPER= {"brain_bg": "#1A1A1A", "lesion_color": "#CCCCCC", "label_color": "#CCCCCC"}
NEGRO_GRE= {"brain_bg": "#444444", "lesion_color": "#080808", "label_color": "#FF6B6B"}   # hemorragia: lesión muy negra

def seq_card(seq_name, intensidad, label_text, **kwargs):
    base = {**intensidad}
    base["seq"] = seq_name
    base["label"] = label_text
    base.update(kwargs)
    return base


# 3. ENCABEZADO Y CONTEXTO COMPACTO
st.title("🧠 Asistente de Isquemia Cerebral")
st.caption("📱 Herramienta de Soporte y Formación Continua para Técnicos Radiólogos y Licenciados en Producción de Bioimágenes")

st.warning(
    "⚠️ **Nota Operativa:** Enfocado en **ACV Isquémico** para identificar derivación inmediata a guardia o hallazgo crónico."
)

st.write("---")

# 4. PANEL INTERACTIVO DE IMÁGENES
st.markdown("### 🎛️ Seleccione los hallazgos visuales de la consola:")

st.markdown("**Secuencias principales** (definen el estadio isquémico):")

dwi = st.selectbox(
    "1. DIFUSIÓN (DWI):",
    ["Hiperintensa (Blanca / Brilla mucho)", "Isointensa (Gris / Normal)", "Hipointensa (Oscura / Negra)"]
)

adc = st.selectbox(
    "2. MAPA DE ADC:",
    ["Hipointensa (Oscura / Negra)", "Levemente Hipointensa (Gris oscura / Intermedia)", "Isointensa (Gris / Normal)", "Hiperintensa (Blanca / Brilla)"]
)

flair = st.selectbox(
    "3. Secuencia FLAIR:",
    ["Isointensa / Normal (No se nota inflamación o brilla el LCR normal)", "Hiperintensa (Blanca / Brilla la corteza/tejido)"]
)

st.markdown("**Secuencia opcional** (solo descarta/confirma sangrado, no afecta el estadio isquémico):")

gre = st.selectbox(
    "4. Secuencia GRE / T2* (Gradiente) — OPCIONAL:",
    [
        "— No evaluada / No tildar —",
        "Isointenso / Normal (sin sangrado)",
        "Hipointenso (Mancha negra / Sangrado)",
    ]
)

# 5. LÓGICA DE DETECCIÓN CON EXPLICACIÓN FISIOPATOLÓGICA INCORPORADA
st.write("---")

if st.button("⚡ Evaluar e Identificar Estadio", type="primary", use_container_width=True):

    # ===================================================================== #
    # A) DIAGNÓSTICO ISQUÉMICO — basado SOLO en DWI, ADC y FLAIR
    # ===================================================================== #
    adc_negra = adc == "Hipointensa (Oscura / Negra)"
    adc_leve = "Levemente Hipointensa" in adc
    adc_hiper = "Hiperintensa" in adc

    # A.1 ISQUEMIA CRÓNICA (>21 días)
    if "Hipointensa" in dwi and adc_hiper and "Hiperintensa" in flair:
        st.info("### 🏛️ ISQUEMIA CRÓNICA (>21 días) — Hallazgo Antiguo")

        with st.expander("🖼️ Ver patrón de señal de referencia", expanded=True):
            render_reference_images([
                seq_card("DWI",   HIPO,     "Hipointensa\n(Negra)"),
                seq_card("ADC",   HIPER,    "Hiperintensa\n(Blanca)"),
                seq_card("FLAIR", HIPER,    "Hiperintensa\n(Gliosis)"),
                seq_card("GRE",   HIPO,     "Normal /\nHipointenso", note="hemosiderina"),
            ])

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI Hipointensa (Negra):** El tejido cerebral muerto ya desapareció por completo y no hay células que atrapen el agua.")
        st.write("* **ADC Hiperintensa (Blanca):** Refleja la total libertad de movimiento del agua (difusión facilitada) al no haber barreras celulares.")
        st.write("* **FLAIR Hiperintensa (Blanca):** Aunque el centro quístico se vuelve negro, todo el borde que rodea a esa cicatriz vieja (la gliosis periférica) sigue brillando con fuerza por la cicatrización glial astrocitaria.")

        st.markdown("**🟢 ACCIÓN DEL TÉCNICO:** Se trata de una cicatriz vieja de hace meses o años. **No requiere enviar a la guardia por este hallazgo**; se procesa y archiva como un estudio ambulatorio normal.")

    # A.2 ISQUEMIA HIPERAGUDA (<6h) -> ¡Urgencia Médica Crítica!
    elif "Hiperintensa" in dwi and adc_negra and "Isointensa" in flair:
        st.success("### ⚡ ISQUEMIA HIPERAGUDA (< 6 horas) — Ventana Terapéutica")

        with st.expander("🖼️ Ver patrón de señal de referencia", expanded=True):
            render_reference_images([
                seq_card("DWI",   HIPER,   "Hiperintensa\n(Blanca ✓)"),
                seq_card("ADC",   HIPO,    "Hipointensa\n(Negra ✓)"),
                seq_card("FLAIR", ISO,     "Normal\n(clave: mismatch)", note="DWI/FLAIR +"),
                seq_card("GRE",   ISO,     "Normal\n(sin sangrado)"),
            ])

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI Hiperintensa (Blanca / Brilla mucho):** El edema citotóxico inicial apaga la bomba sodio-potasio, las células se hinchan y el agua queda atrapada en el espacio intracelular, restringiendo su movimiento de inmediato.")
        st.write("* **ADC Hipointensa (Negra):** Es la confirmación matemática y física estricta de que el brillo en la Difusión es una verdadera restricción aguda por falta de oxígeno.")
        st.write("* **FLAIR Isointensa / Normal:** **Es la clave del descalce (mismatch) DWI/FLAIR**. El infarto es tan extremadamente reciente (menos de 6 horas) que el líquido aún no ha tenido tiempo de acumularse en el espacio extracelular (edema vasogénico), por lo que la secuencia FLAIR no nota la inflamación todavía.")

        st.markdown("**🔴 ACCIÓN DEL TÉCNICO:** El paciente está en la ventana de tiempo crítica para recibir tratamiento y salvar el cerebro. **Enviar urgente a la Guardia médica hospitalaria** e informar al Radiólogo.")

    # A.3 ISQUEMIA AGUDA (6h a 3 días) -> ¡Urgencia Médica!
    elif "Hiperintensa" in dwi and adc_negra and "Hiperintensa" in flair:
        st.success("### 🚨 ISQUEMIA AGUDA (6h a 3 días) — Infarto Establecido")

        with st.expander("🖼️ Ver patrón de señal de referencia", expanded=True):
            render_reference_images([
                seq_card("DWI",   HIPER,     "Hiperintensa\n(Blanca)"),
                seq_card("ADC",   HIPO,      "Hipointensa\n(Negra)"),
                seq_card("FLAIR", HIPER,     "Hiperintensa\n(edema vasog.)"),
                seq_card("GRE",   LEV_HIPER, "Lev. Hiperintenso\n(edema sutil)"),
            ])

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI / ADC (Brillante / Negro):** Persiste el daño celular agudo severo con restricción del movimiento del agua intracelular.")
        st.write("* **FLAIR Hiperintensa (Blanca):** El infarto ya lleva horas desarrollándose. Las células empiezan a sufrir daños estructurales y el agua se acumula en el espacio libre (edema vasogénico establecido), haciendo que la corteza brille de forma evidente.")

        st.markdown("**🔴 ACCIÓN DEL TÉCNICO:** Aunque ya pasó la ventana hiperaguda inicial, sigue siendo un evento agudo que requiere atención prioritaria y urgente en la guardia hospitalaria.")

    # A.4 ISQUEMIA SUBAGUDA (3 a 21 días) — Fase de Transición
    elif "Hiperintensa" in dwi and adc_leve and "Hiperintensa" in flair:
        st.warning("### ⏳ ISQUEMIA SUBAGUDA (3 a 21 días) — Fase de Transición")

        with st.expander("🖼️ Ver patrón de señal de referencia", expanded=True):
            render_reference_images([
                seq_card("DWI",   HIPER,    "Hiperintensa\n(fading)"),
                seq_card("ADC",   LEV_HIPO, "Lev. Hipointensa\n(pseudonorm.)", note="↑ ADC gradual"),
                seq_card("FLAIR", HIPER,    "Hiperintensa\n(persiste)"),
                seq_card("GRE",   HIPER,    "Hiperintenso\n(cambios metab.)"),
            ])

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI / ADC:** La restricción empieza a disminuir lentamente (efecto de desvanecimiento o 'fading'). El mapa de ADC ya no se ve tan negro.")
        st.write("* **FLAIR:** Se mantiene brillante debido a la presencia constante de edema vasogénico y desintegración del tejido.")

        st.markdown("**🟡 ACCIÓN DEL TÉCNICO:** Es una lesión en evolución. Se debe coordinar con el médico radiólogo para evaluar si requiere priorización en el informe según el estado del paciente.")

    else:
        st.info("### ℹ️ Combinación no específica")
        st.write("Los hallazgos seleccionados en DWI, ADC y FLAIR no se ajustan exactamente a los patrones clásicos automatizados de esta herramienta. Por favor, realice una correlación clínica completa y consulte al médico radiólogo de guardia.")

    # ===================================================================== #
    # B) ALERTA DE SANGRADO — GRE opcional, evaluada por separado
    #    Si no se tildó nada, no interfiere en el diagnóstico isquémico.
    # ===================================================================== #
    if "Hipointenso" in gre or "Mancha negra" in gre:
        st.write("---")
        st.error("### 🚨 ALERTA ADICIONAL: GRE compatible con SANGRADO / COMPONENTE HEMORRÁGICO")

        with st.expander("🖼️ Ver patrón de señal de referencia", expanded=True):
            render_reference_images([
                seq_card("DWI",   HIPER,    "Variable\n(según estadio)"),
                seq_card("ADC",   HIPO,     "Variable\n(según estadio)"),
                seq_card("FLAIR", HIPER,    "Variable"),
                seq_card("GRE",   NEGRO_GRE,"⚠️ Mancha\nnegra (bloom)", note="hemorragia"),
            ])

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **GRE Hipointenso (Mancha negra drástica):** Delata la presencia de productos de degradación de la hemoglobina (susceptibilidad magnética). Puede tratarse de un sangrado, una transformación hemorrágica de un infarto o microsangrados crónicos.")

        st.markdown("**🛑 ACCIÓN DEL TÉCNICO:** Este hallazgo es independiente del estadio isquémico. **Avisar al médico radiólogo de guardia** antes de bajar al paciente de la camilla, ya que puede cambiar la conducta terapéutica.")

# 6. SECCIÓN EDUCATIVA: TABLA RESUMEN SIEMPRE VISIBLE AL FINAL
st.write("---")
with st.expander("📊 Tabla Resumen — Señales por Estadio"):
    st.markdown("""
| Estadio | DWI | ADC | FLAIR | GRE/T2* |
|---|---|---|---|---|
| **Hiperagudo** (<6h) | ⬜ Blanca | ⬛ Negra | ▪️ Normal | ▪️ Normal |
| **Agudo** (6h–3d) | ⬜ Blanca | ⬛ Negra | ⬜ Blanca | 🔲 Lev. blanca |
| **Subagudo** (3–21d) | ⬜ Blanca | 🔲 Gris oscuro | ⬜ Blanca | ⬜ Blanca |
| **Crónico** (>21d) | ⬛ Negra | ⬜ Blanca | ⬜ Blanca* | ▪️ Normal/negro |
| **Hemorragia** | ⬜/▪️ | ⬛/▪️ | ⬜ | 🔴 Mancha negra |

*En crónico: el centro es negro (quiste), el borde es blanco (gliosis)
""")
