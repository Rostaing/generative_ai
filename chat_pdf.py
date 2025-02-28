import streamlit as st
import ollama
import pymupdf4llm
import os

# Configuration de l'interface utilisateur Streamlit
st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="🤖",
    # layout="wide",
    initial_sidebar_state="expanded",
)

# Personnalisation du thème Streamlit
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #262730;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #31333F;
    }
    .stTextInput > div > div > input {
        border: 2px solid #4F8BF9;
        border-radius: 8px;
        padding: 12px;
    }
    .stButton > button {
        background-color: #4F8BF9;
        color: white;
        border-radius: 8px;
        padding: 2px 5px;
    }
    .stTextArea > div > div > textarea {
        border: 2px solid #4F8BF9;
        border-radius: 8px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Barre latérale
with st.sidebar:
    st.title("Configuration")
    st.markdown("Personnalisez votre chatbot PDF.")

    model_name = st.selectbox(
        "Choisissez un modèle Ollama :",
        options=["qwen2.5:latest", "llama3.2:latest"],  # Ajoutez d'autres modèles si nécessaire
        index=0,  # Sélectionne le premier modèle par défaut
    )

    uploaded_file = st.file_uploader("Téléchargez votre fichier PDF :", type="pdf")

    if uploaded_file:
        st.write("Fichier PDF actuel:")
        st.write(uploaded_file.name) # Display filename

    system_prompt = st.text_area(
        "Prompt Système (facultatif) :",
        value="Vous êtes un assistant utile spécialisé dans l'extraction d'informations à partir de documents PDF.",
        height=150,
    )

    st.markdown("---")
    st.markdown("Développé par Rostaing AI")

# Corps principal de l'application
st.html("<h1><marquee>Chatbot PDF intelligent 🤖 - Rostaing AI</marquee></h1>")
# st.html("<hr>")

# Ajouter le bouton de nettoyage du chat
col1, col2 = st.columns([5, 1])  # Adjust ratio as needed

with col1:
    pass # Empty column, just for spacing

with col2:
    if st.button("Effacer le chat", key="clear_chat"):
        st.session_state.messages = []

if uploaded_file is not None:
    # Sauvegarder temporairement le fichier PDF
    file_path = "temp.pdf"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extraction du texte du PDF
    try:
        md_text = pymupdf4llm.to_markdown(file_path)
    except Exception as e:
        st.error(f"Erreur lors de l'extraction du texte du PDF : {e}")
        md_text = ""

    # Interface de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Posez votre question :"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                completion = ollama.chat(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"$context: Réponds à la question posée en tenant compte du contexte de contenu suivant:\n{md_text}\n\n$query:{prompt}"}
                    ],
                    stream=True
                )

                for chunk in completion:
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)  # Afficher la réponse finale
            except Exception as e:
                full_response = f"Une erreur s'est produite : {e}"
                message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Nettoyer le fichier temporaire
    if os.path.exists(file_path):
        os.remove(file_path)

else:
    st.info("Veuillez télécharger un fichier PDF pour commencer.")