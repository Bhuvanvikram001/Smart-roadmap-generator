import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Roadmap Generator")

st.title("🚀 AI Roadmap Generator (Hugging Face)")

API_URL = "https://router.huggingface.co/hf-inference/models/google/gemma-2b-it"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}

def generate_text(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()

    if isinstance(data, list):
        return data[0]["generated_text"]

    return data

goal = st.text_input("Enter Your Career Goal")

if st.button("Generate Roadmap"):
    if goal:
        with st.spinner("Generating roadmap..."):
            result = generate_text(
                f"Create a detailed roadmap to become {goal} with timeline, tools, and projects."
            )
            st.write(result)
    else:
        st.warning("Please enter a goal")
