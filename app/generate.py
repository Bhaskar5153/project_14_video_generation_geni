import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", default="")

client = genai.Client(api_key=API_KEY)

prompt = """
3D animation, close up, small squirrel fast dribbling a glowing basketball, large rusty robot trying to block, high speed, dynamic camera angles, cinematic, cartoon, vibrant colors."""

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("funny.mp4")
print("Generated video saved to dialogue_example.mp4")
