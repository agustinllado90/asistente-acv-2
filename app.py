import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Asistente ACV",
    page_icon="🧠",
    layout="centered"
)

# 2. ENCABEZADO Y CONTEXTO COMPACTO
st.title("🧠 Asistente de Isquemia Cerebral")
st.caption("📱 Herramienta de Soporte y Formación Continua para Técnicos Radiólogos y Licenciados en Producción de Bioimágenes")

st.warning(
    "⚠️ **Nota Operativa:** Enfocado en **ACV Isquémico** para identificar derivación inmediata a guardia o hallazgo crónico."
)

st.write("---")

# 3. PANEL INTERACTIVO DE IMÁGENES
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

# 4. LÓGICA DE DETECCIÓN CON EXPLICACIÓN FISIOPATOLÓGICA INCORPORADA
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

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI Hipointensa (Negra):** El tejido cerebral muerto ya desapareció por completo y no hay células que atrapen el agua.")
        st.write("* **ADC Hiperintensa (Blanca):** Refleja la total libertad de movimiento del agua (difusión facilitada) al no haber barreras celulares.")
        st.write("* **FLAIR Hiperintensa (Blanca):** Aunque el centro quístico se vuelve negro, todo el borde que rodea a esa cicatriz vieja (la gliosis periférica) sigue brillando con fuerza por la cicatrización glial astrocitaria.")

        st.markdown("**🟢 ACCIÓN DEL TÉCNICO:** Se trata de una cicatriz vieja de hace meses o años. **No requiere enviar a la guardia por este hallazgo**; se procesa y archiva como un estudio ambulatorio normal.")

    # A.2 ISQUEMIA HIPERAGUDA (<6h) -> ¡Urgencia Médica Crítica!
    elif "Hiperintensa" in dwi and adc_negra and "Isointensa" in flair:
        st.success("### ⚡ ISQUEMIA HIPERAGUDA (< 6 horas) — Ventana Terapéutica")

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI Hiperintensa (Blanca / Brilla mucho):** El edema citotóxico inicial apaga la bomba sodio-potasio, las células se hinchan y el agua queda atrapada en el espacio intracelular, restringiendo su movimiento de inmediato.")
        st.write("* **ADC Hipointensa (Negra):** Es la confirmación matemática y física estricta de que el brillo en la Difusión es una verdadera restricción aguda por falta de oxígeno.")
        st.write("* **FLAIR Isointensa / Normal:** **Es la clave del descalce (mismatch) DWI/FLAIR**. El infarto es tan extremadamente reciente (menos de 6 horas) que el líquido aún no ha tenido tiempo de acumularse en el espacio extracelular (edema vasogénico), por lo que la secuencia FLAIR no nota la inflamación todavía.")

        st.markdown("**🔴 ACCIÓN DEL TÉCNICO:** El paciente está en la ventana de tiempo crítica para recibir tratamiento y salvar el cerebro. **Enviar urgente a la Guardia médica hospitalaria** e informar al Radiólogo.")

    # A.3 ISQUEMIA AGUDA (6h a 3 días) -> ¡Urgencia Médica!
    elif "Hiperintensa" in dwi and adc_negra and "Hiperintensa" in flair:
        st.success("### 🚨 ISQUEMIA AGUDA (6h a 3 días) — Infarto Establecido")

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI / ADC (Brillante / Negro):** Persiste el daño celular agudo severo con restricción del movimiento del agua intracelular.")
        st.write("* **FLAIR Hiperintensa (Blanca):** El infarto ya lleva horas desarrollándose. Las células empiezan a sufrir daños estructurales y el agua se acumula en el espacio libre (edema vasogénico establecido), haciendo que la corteza brille de forma evidente.")

        st.markdown("**🔴 ACCIÓN DEL TÉCNICO:** Aunque ya pasó la ventana hiperaguda inicial, sigue siendo un evento agudo que requiere atención prioritaria y urgente en la guardia hospitalaria.")

    # A.4 ISQUEMIA SUBAGUDA (3 a 21 días) — Fase de Transición
    elif "Hiperintensa" in dwi and adc_leve and "Hiperintensa" in flair:
        st.warning("### ⏳ ISQUEMIA SUBAGUDA (3 a 21 días) — Fase de Transición")

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

        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **GRE Hipointenso (Mancha negra drástica):** Delata la presencia de productos de degradación de la hemoglobina (susceptibilidad magnética). Puede tratarse de un sangrado, una transformación hemorrágica de un infarto o microsangrados crónicos.")

        st.markdown("**🛑 ACCIÓN DEL TÉCNICO:** Este hallazgo es independiente del estadio isquémico. **Avisar al médico radiólogo de guardia** antes de bajar al paciente de la camilla, ya que puede cambiar la conducta terapéutica.")
