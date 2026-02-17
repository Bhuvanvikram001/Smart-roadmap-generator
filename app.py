import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Roadmap Generator")

st.title("🚀 AI Roadmap Generator (Hugging Face)")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

goal = st.text_input("Enter Your Career Goal")

if st.button("Generate Roadmap"):
    if goal:
        with st.spinner("Generating..."):
            output = query({
                "inputs": f"Create a detailed roadmap to become {goal} with timeline and projects."
            })

            if isinstance(output, list):
                st.write(output[0]["generated_text"])
            else:
                st.write(output)
    else:
        st.warning("Please enter a goal")
