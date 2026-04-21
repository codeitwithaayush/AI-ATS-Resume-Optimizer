import os
import json
from groq import Groq
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

def analyze_resume(resume_text, jd_text):
    # Retrieve key from environment (passed from Streamlit sidebar)
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return {"error": "Groq API Key is missing. Enter it in the sidebar."}

    client = Groq(api_key=api_key)
    
    try:
        # We use Llama 3.3 70B - it's very smart and free on Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(jd=jd_text, resume_text=resume_text)}
            ],
            response_format={"type": "json_object"} # Forces the AI to give us valid JSON
        )
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        return {"error": f"Groq Error: {str(e)}"}