
import streamlit as st
import json

st.set_page_config(page_title="Prompt Builder", page_icon="🎮", layout="wide")

# --- Login via email check ---
ALLOWED_EMAILS = ["alice.cuccia94@gmail.com"]
if not st.experimental_user.email or st.experimental_user.email not in ALLOWED_EMAILS:
    st.error("🔒 Accesso riservato. Questa email non è autorizzata.")
    st.stop()

st.title("🎮 Daje, forte 'sto prompt builder!")

st.markdown("""
Crea prompt strutturati, utili per task complessi, analisi e automazioni guidate.  
Compila i campi qui sotto e ottieni un prompt pronto all'uso in formato testuale e JSON.
""")

# Funzione per generare il prompt testuale
def generate_prompt(role, department, task, task_description, criteria, references, style):
    criteria_txt = "\n".join([f"- {c['name']}: {c['description']}" for c in criteria])
    ref_txt = f"Based on: {references.get('title')} by {references.get('author')} ({references.get('year')})\nKey insights: {references.get('key_insights')}" if references.get("title") else ""

    prompt_text = f"""You are a {role} in the {department} department.
Your task is: {task}
Details: {task_description}

{ref_txt}

Evaluation criteria:
{criteria_txt}

Style: {style}
"""
    return prompt_text

# Form principale
with st.form("prompt_form"):
    st.header("🔧 Configura il tuo prompt")

    prompt_base = st.text_input("🎯 Prompt base", "Develop a tailored [OUTPUT] aligned with the user’s individual needs...")
    role = st.text_input("👤 Ruolo professionale", placeholder="Es: Expert-level sales strategist")
    department = st.text_input("🏢 Dipartimento", placeholder="Es: Sales")
    task = st.text_input("🛠 Task", placeholder="Es: Create a Sales Funnel Analysis")
    task_description = st.text_area("📝 Descrizione del Task", placeholder="Spiega in dettaglio cosa deve fare l'intelligenza artificiale")

    style = st.selectbox("🎨 Stile del Prompt", ["Tecnico", "Persuasivo", "Formale", "Storytelling", "Creativo"])

    with st.expander("📚 Riferimenti chiave (opzionali)"):
        ref_title = st.text_input("Titolo riferimento")
        ref_author = st.text_input("Autore")
        ref_year = st.text_input("Anno")
        ref_keyinsights = st.text_area("Insight principali (separati da virgola)")

    with st.expander("📏 Criteri di valutazione (massimo 3)"):
        criteria = []
        for i in range(1, 4):
            name = st.text_input(f"Nome criterio #{i}", key=f"crit_name_{i}")
            desc = st.text_area(f"Descrizione criterio #{i}", key=f"crit_desc_{i}")
            if name and desc:
                criteria.append({"name": name, "description": desc})

    submitted = st.form_submit_button("🚀 Genera Prompt")

    if submitted:
        if not role or not task:
            st.warning("⚠️ Inserisci almeno ruolo e task per generare il prompt.")
        else:
            references = {
                "title": ref_title,
                "author": ref_author,
                "year": ref_year,
                "key_insights": ref_keyinsights
            }

            full_prompt = generate_prompt(role, department, task, task_description, criteria, references, style)

            output_json = {
                "prompt": prompt_base,
                "role": role,
                "department": department,
                "task": task,
                "task_description": task_description,
                "style": style,
                "evaluation_criteria": criteria,
                "references": references
            }

            st.subheader("📄 Prompt finale")
            st.code(full_prompt, language="markdown")

            st.subheader("🧾 Prompt JSON")
            st.json(output_json)

            st.download_button("📥 Scarica JSON", data=json.dumps(output_json, indent=2), file_name="prompt.json")
