import openai
from fpdf import FPDF
from PyPDF2 import PdfReader
import streamlit as st
import base64
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.pdf">Download {file_label}</a>'
    return href

def generate_questions_from_notes(notes):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Create practice questions based on these notes: \n\n" + notes,
        max_tokens=1000
    )
    return response.choices[0].text

def read_pdf(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            # Read the PDF file directly from the UploadedFile object
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    return text


def create_pdf(questions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    for question in questions.split('\n'):
        pdf.cell(0, 10, txt=question, ln=True)
    pdf.output("practice_test.pdf")

def main():    
    st.subheader("Your documents")
    pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Processing"):
            if pdf_docs:
                notes = read_pdf(pdf_docs)
                questions = generate_questions_from_notes(notes)
                create_pdf(questions)
                st.success("PDF practice test generated successfully!")
                st.write("Download your PDF practice test:")
                st.markdown(get_binary_file_downloader_html("practice_test.pdf", 'Practice Test PDF'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
