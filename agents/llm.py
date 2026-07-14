import os
import requests
from dotenv import load_dotenv

load_dotenv()

def call_llm(prompt):
    api_key= os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Error: Groq API Key Missing"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions",  
                                 headers=headers, 
                                 json=payload,
                                 timeout=30)
        
        print("Status Code:", response.status_code)

        data = response.json()
        print("Response Data:", data)

        if response.status_code != 200:
            return f"Groq API Error: {data}"
        
        if "choices" not in data:
            return f"Invalid response structure: {data}"
        
        return data["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        return f"exception during llm call: {str(e)}"
   

