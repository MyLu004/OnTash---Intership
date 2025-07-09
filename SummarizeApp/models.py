import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

st.title("📚 Article Summarizer Kinoko")

input_text = st.text_area("Paste your article or text here")

if st.button("Summarize"):
    llm = Ollama(model="llama3.2:1b")

    custom_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a helpful assistant.

Please summarize the following text in **this exact format**:

- Bullet Point 1
- Bullet Point 2
- Bullet Point 3

Then give a TL;DR sentence.

Text:
{text}

Summary:
"""
)

chain = LLMChain(llm=llm, prompt=custom_prompt)
summary = chain.run({"text": input_text})

st.subheader("Summary kinoko1")
st.write(summary)
