import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


client = Groq()


filename = os.path.dirname(__file__) + "/audio.m4a"

with open(filename, "rb") as file:

    transcription = client.audio.transcriptions.create(

        file = (filename, file.read()),
        model="whisper-large-v3",
        response_format="text",
        # prompt="Fais-moi un résumé de cet audio.",
        # language="en",
        temperature=0.0
    )

    print(transcription)