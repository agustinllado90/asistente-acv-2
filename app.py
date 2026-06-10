import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Asistente ACV", 
    page_icon="🧠", 
    layout="centered"
)

# 2. ENCABEZADO Y CONTEXTO COMPACTO
st.title("🧠 Asistente de Isquemia Cerebral")
st.caption("📱 Herramienta de Soporte y Formación Continua para Técnicos Radiólogos")

st.warning(
    "⚠️ **Nota Operativa:** Enfocado en **ACV Isquémico** para identificar derivación inmediata a guardia o hallazgo crónico."
)

st.write("---")

# 3. PANEL INTERACTIVO DE IMÁGENES
st.markdown("### 🎛️ Seleccione los hallazgos visuales de la consola:")

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

gre = st.selectbox(
    "4. Secuencia GRE / T2* (Gradiente):",
    ["Isointenso (Normal / Gris)", "Isointenso a levemente Hiperintenso (Gris claro)", "Hiperintenso (Blanco)", "Hipointenso (Mancha negra de artefacto)"]
)

# 4. LÓGICA DE DETECCIÓN CON EXPLICACIÓN FISIOPATOLÓGICA INCORPORADA
st.write("---")

if st.button("⚡ Evaluar e Identificar Estadio", type="primary", use_container_width=True):
    
    # A. ISQUEMIA CRÓNICA (>21 días)
    if "Hipointensa" in dwi and "Hiperintensa" in adc and "Hiperintensa" in flair and ("Normal" in gre or "Hipointenso" in gre):
        st.info("### 🏛️ ISQUEMIA CRÓNICA (>21 días) — Hallazgo Antiguo")
        
        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI Hipointensa (Negra):** El tejido cerebral muerto ya desapareció por completo y no hay células que atrapen el agua.")
        st.write("* **ADC Hiperintensa (Blanca):** Refleja la total libertad de movimiento del agua (difusión facilitada) al no haber barreras celulares.")
        st.write("* **FLAIR Hiperintensa (Blanca):** Aunque el centro quístico se vuelve negro, todo el borde que rodea a esa cicatriz vieja (la gliosis periférica) sigue brillando con fuerza por la cicatrización glial astrocitaria.")
        st.write("* **GRE Normal o Hipointensa:** La posible caída de señal o mancha negra no es un sangrado actual, sino un efecto de susceptibilidad magnética causado por depósitos crónicos de hemosiderina (sangre vieja atrapada en la cicatriz) o por el borde de la cavidad quística.")
        
        st.markdown("**🟢 ACCIÓN DEL TÉCNICO:** Se trata de una cicatriz vieja de hace meses o años. **No requiere enviar a la guardia por este hallazgo**; se procesa y archiva como un estudio ambulatorio normal.")

    # B. FRENO DE SEGURIDAD: Sospecha de Sangrado o Transformación Hemorrágica Aguda
    elif "Mancha negra" in gre and ("Hiperintensa" in dwi or "Hipointensa" in adc or "Levemente Hipointensa" in adc):
        st.error("### 🚨 ALERTA: COMPATIBLE CON HEMORRAGIA / TRANSFORMACIÓN AGUDA")
        
        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **GRE Hipointenso (Mancha negra drástica):** Delata la presencia de productos de degradación de la hemoglobina fresca. Al combinarse con una lesión reciente (DWI brillante o ADC negro), nos avisa que el infarto está sufriendo una complicación hemorrágica activa y peligrosa en este mismo momento.")
        
        st.markdown("**🛑 ACCIÓN DEL TÉCNICO:** Invalida de inmediato el protocolo estándar de isquemia pura. **Avisar de forma urgente al médico radiólogo de guardia** antes de bajar al paciente de la camilla.")

    # C. ISQUEMIA HIPERAGUDA (<6h) -> ¡Urgencia Médica Crítica!
    elif "Hiperintensa" in dwi and "Hipointensa" in adc and "Isointensa" in flair and "Isointenso (Normal" in gre:
        st.success("### ⚡ ISQUEMIA HIPERAGUDA (< 6 horas) — Ventana Terapéutica")
        
        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI Hiperintensa (Blanca / Brilla mucho):** El edema citotóxico inicial apaga la bomba sodio-potasio, las células se hinchan y el agua queda atrapada en el espacio intracelular, restringiendo su movimiento de inmediato.")
        st.write("* **ADC Hipointensa (Negra):** Es la confirmación matemática y física estricta de que el brillo en la Difusión es una verdadera restricción aguda por falta de oxígeno.")
        st.write("* **FLAIR Isointensa / Normal:** **Es la clave del descalce (mismatch) DWI/FLAIR**. El infarto es tan extremadamente reciente (menos de 6 horas) que el líquido aún no ha tenido tiempo de acumularse en el espacio extracelular (edema vasogénico), por lo que la secuencia FLAIR no nota la inflamación todavía.")
        st.write("* **GRE Normal (Gris):** No hay cambios estructurales ni depósitos hemorrágicos basales.")
        
        st.markdown("**🔴 ACCIÓN DEL TÉCNICO:** El paciente está en la ventana de tiempo crítica para recibir tratamiento y salvar el cerebro. **Enviar urgente a la Guardia médica hospitalaria** e informar al Radiólogo.")

    # D. ISQUEMIA AGUDA (6h a 3 días) -> ¡Urgencia Médica!
    elif "Hiperintensa" in dwi and "Hipointensa" in adc and "Hiperintensa" in flair and "levemente Hiperintenso" in gre:
        st.success("### 🚨 ISQUEMIA AGUDA (6h a 3 días) — Infarto Establecido")
        
        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI / ADC (Brillante / Negro):** Persiste el daño celular agudo severo con restricción del movimiento del agua intracelular.")
        st.write("* **FLAIR Hiperintensa (Blanca):** El infarto ya lleva horas desarrollándose. Las células empiezan a sufrir daños estructurales y el agua se acumula en el espacio libre (edema vasogénico establecido), haciendo que la corteza brille de forma evidente.")
        st.write("* **GRE Levemente Hiperintenso (Gris claro):** A diferencia de la etapa hiperaguda, el edema vasogénico macroscópico ya comenzó a manifestarse sutilmente en esta secuencia, alterando levemente la escala de grises hacia tonos más claros.")
        
        st.markdown("**🔴 ACCIÓN DEL TÉCNICO:** Aunque ya pasó la ventana hiperaguda inicial, sigue siendo un evento agudo que requiere atención prioritaria y urgente en la guardia hospitalaria.")

    # E. ISQUEMIA SUBAGUDA (3 a 21 días) — Fase de Transición
    elif "Hiperintensa" in dwi and "Levemente Hipointensa" in adc and "Hiperintensa" in flair and "Hiperintenso" in gre:
        st.warning("### ⏳ ISQUEMIA SUBAGUDA (3 a 21 días) — Evolución Intermedia")
        
        st.markdown("#### 🔬 ¿Por qué se ve de esta manera?")
        st.write("* **DWI Hiperintensa (Blanca):** Se mantiene la señal brillante en difusión debido a la persistencia del fenómeno celular o efectos intrínsecos de permeabilidad de las membranas que siguen alteradas.")
        st.write("* **ADC Levemente Hipointensa (Gris oscura):** Refleja la transición del tejido. La restricción severa del agua empieza a ceder paulatinamente a medida que avanza la lisis celular (las células muertas se rompen y el líquido empieza a liberarse lentamente).")
        st.write("* **FLAIR / GRE Francamente Hiperintensos (Blancos):** El edema vasogénico y la gliosis inflamatoria llegan a su punto máximo de volumen e intensidad, haciendo que ambas secuencias brillen intensamente en la zona afectada.")
        
        st.markdown("**🟡 ACCIÓN DEL TÉCNICO:** Es un cuadro en evolución intermedia. No es una urgencia de 'código rojo' de minutos, pero el paciente debe ser derivado a una consulta médica programada o revisión de guardia según su estado clínico actual.")

    # F. COMBINACIONES ATÍPICAS
    else:
        st.error("### 🔍 Patrón Mixto / Combinación No Lógica")
        st.write("Las opciones seleccionadas no coinciden con la evolución temporal clásica de un infarto. Por favor, reevalúe detalladamente las intensidades de señal directamente en la consola de adquisición para descartar artefactos o errores de selección visual.")
