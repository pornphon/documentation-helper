import streamlit as st
from backend.core import run_llm

st.header("Langchain00dddd")
prompt=st.text_input("Prompt",placeholder="Enter your prompt here...")

if (prompt):
    with st.spinner("Generate response..."):
        generated_response=run_llm(query=prompt)
        source=set([doc.metadata["source"]] for doc in generated_response["source_documents"])

        formated_response=