import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA (Ajustada para pantallas pequeñas y grandes)
st.set_page_config(
    page_title="Asistente ACV", 
    page_icon="🧠", 
    layout="centered"
)

# 2. ENCABEZADO Y CONTEXTO COMPACTO
st.title("🧠 Asistente de Isquemia Cerebral")
st.caption("📱 Optimizado para uso en celulares, tablets y PC")

st.warning(
    "⚠️ **Nota Operativa:** Enfocado en **ACV Isquémico** para identificar derivación inmediata a guardia o hallazgo crónico."
)

st.write("---")

# 3. PANEL INTERACTIVO DE IMÁGENES (Campos grandes para pantallas táctiles)
st.markdown("### 🎛️ Seleccione los hallazgos visuales:")

dwi = st.selectbox(
    "1. DIFUSIÓN (DWI):",
    ["Hiperintensa (Blanca / Brilla mucho)", "Isointensa (Gris / Normal)", "Hipointensa (Oscura / Negra)"]
)

adc = st.selectbox(
    "2. MAPA DE ADC:",
    ["Hipointensa (Oscura / Negra)", "Isointensa (Gris / Normal)", "Hiperintensa (Blanca / Brilla)"]
)

flair = st.selectbox(
    "3. Secuencia FLAIR:",
    ["Isointensa / Normal (No se nota inflamación o brilla el LCR normal)", "Hiperintensa (Blanca / Brilla la corteza/tejido)"]
)

gre = st.selectbox(
    "4. Secuencia GRE / T2* (Gradiente):",
    ["Isointenso (Normal / Gris)", "Isointenso a levemente Hiperintenso (Gris claro)", "Hiperintenso (Blanco)", "Hipointenso (Mancha negra de artefacto)"]
)

# 4. LÓGICA DE DETECCIÓN ORIENTADA AL FLUJO DE TRABAJO
st.write("---")

if st.button("⚡ Evaluar e Identificar Estadio", type="primary", use_container_width=True):
    
    # A. Freno de seguridad: Sospecha de Sangrado en GRE
    if "Mancha negra" in gre:
        st.error("### 🚨 ALERTA: COMPATIBLE CON HEMORRAGIA")
        st.write("**Visual:** Caída drástica de señal (mancha negra en GRE). Invalida protocolo de isquemia pura.")
        st.markdown("**🛑 ACCIÓN:** Avisar de inmediato al médico radiólogo de guardia antes de bajar al paciente.")

    # B. Isquemia Hiperaguda (<6h) -> ¡Urgencia Médica!
    elif "Hiperintensa" in dwi and "Hipointensa" in adc and "Isointensa" in flair and "Normal" in gre:
        st.success("### ⚡ ISQUEMIA HIPERAGUDA (< 6 horas)")
        st.write("**Visual:** Brilla en DWI, negro en ADC. **FLAIR normal** (infarto menor a 6 horas).")
        st.markdown("**🔴 ACCIÓN:** Ventana terapéutica crítica. **Enviar urgente a la Guardia**.")

    # C. Isquemia Aguda (6h a 3 días) -> ¡Urgencia Médica!
    elif "Hiperintensa" in dwi and "Hipointensa" in adc and "Hiperintensa" in flair and "levemente Hiperintenso" in gre:
        st.success("### 🚨 ISQUEMIA AGUDA (6h a 3 días)")
        st.write("**Visual:** Brilla en DWI, negro en ADC y **ya brilla en FLAIR**.")
        st.markdown("**🔴 ACCIÓN:** Requiere atención urgente en la guardia médica hospitalaria.")

    # D. Isquemia Subaguda (7 a 21 días)
    elif ("Hiperintensa" in dwi or "Isointensa" in dwi) and "Hiperintensa" in adc and "Hiperintensa" in flair and "Hiperintenso" in gre:
        st.warning("### ⏳ ISQUEMIA SUBAGUDA (7 a 21 días)")
        st.write("**Visual:** ADC y GRE brillan (células rotas, líquido libre). FLAIR brilla por cicatrización.")
        st.markdown("**🟡 ACCIÓN:** Evolución intermedia. Derivar a consulta programada o revisión según clínica.")

    # E. Isquemia Crónica (>21 días)
    elif "Hipointensa" in dwi and "Hiperintensa" in adc and "Isointensa" in flair and "Normal" in gre:
        st.info("### 🏛️ ISQUEMIA CRÓNICA (>21 días)")
        st.write("**Visual:** Negro en DWI, blanco en ADC. Tejido muerto reemplazado por líquido (cicatriz vieja).")
        st.markdown("**🟢 ACCIÓN:** Hallazgo antiguo. **No requiere enviar a la guardia**. Trámite ambulatorio normal.")

    # F. Combinaciones no lógicas o erróneas
    else:
        st.error("### 🔍 Patrón Mixto / Error")
        st.write("Las opciones no coinciden con la evolución típica. Verifica los tonos en la consola.")
