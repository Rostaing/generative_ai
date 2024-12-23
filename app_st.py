import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import base64

# Charger les variables d'environnement
load_dotenv()

# Fonction pour encoder l'image en base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Initialiser Groq Client
client = Groq()

# Interface utilisateur Streamlit
st.header("Reconnaissance et détection d’objets: Analyse d'image avec LLaMA 3.2 Vision.")

# Télécharger une image
uploaded_image = st.file_uploader("Téléchargez une image (JPEG/WEBP)", type=["jpg", "jpeg", "webp"])

if uploaded_image:
    # Afficher l'image
    st.sidebar.image(uploaded_image, caption="Image téléchargée", use_container_width=True)

    # Champ de texte pour la question
    question = st.text_input("Posez une question à propos de l'image :")

    if st.button("Analyser l'image"):
        if question.strip() == "":
            st.warning("Veuillez entrer une question avant d'analyser l'image.")
        else:
            # Encoder l'image en base64
            base64_image = encode_image(uploaded_image)

            # Envoyer une requête au modèle
            st.write("Analyse en cours...")
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": question},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-90b-vision-preview",
                    temperature=0,
                    max_tokens=1024,
                    top_p=1,
                )

                # Afficher la réponse du modèle
                response = chat_completion.choices[0].message.content
                st.subheader("Réponse du modèle :")
                st.write(response)

            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")