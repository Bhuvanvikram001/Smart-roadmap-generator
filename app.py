import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Roadmap Generator")

st.title("🚀 AI Roadmap Generator (Hugging Face)")

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}

def query(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # 🔍 Debug info
    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    try:
        return response.json()
    except Exception:
        return f"Invalid JSON response: {response.text}"

goal = st.text_input("Enter Your Career Goal")

if st.button("Generate Roadmap"):
    if goal:
        with st.spinner("Generating roadmap..."):
            result = query(
                f"Create a detailed roadmap to become {goal} with timeline and projects."
            )

            if isinstance(result, list):
                st.write(result[0]["generated_text"])
            else:
                st.write(result)
    else:
        st.warning("Please enter a goal")
