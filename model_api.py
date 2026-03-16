from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

def query_model(prompt):
    try:
        completion = client.chat.completions.create(
            model="qwen/qwen2.5-coder-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=1000
        )

        result = completion.choices[0].message.content

        # Remove reasoning blocks
        if "<think>" in result:
            result = result.split("</think>")[-1]

        return result.strip()

    except Exception as e:
        print("Model API Error:", e)
        return "Workout plan generation failed."