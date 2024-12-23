from groq import Groq
from dotenv import load_dotenv
import base64

load_dotenv()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "images/img5.webp"

# Getting the base64 string
base64_image = encode_image(image_path)

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Qu'y a-t-il dans cette image ?"},
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

print(chat_completion.choices[0].message.content)