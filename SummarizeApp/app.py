import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

st.title("📚 Article Summarizer Kinoko")

input_text = st.text_area("Paste your article or text here")

if st.button("Summarize"):
    llm = Ollama(model="llama3.2:1b")
    chain = load_summarize_chain(llm, chain_type="stuff")
    docs = [Document(page_content=input_text)]
    summary = chain.run(docs)
    st.subheader("Summary")
    st.write(summary)
