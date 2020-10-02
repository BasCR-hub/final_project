import streamlit as st
import pdftotext
import re
import os

st.title('Search pdf app')
st.write('test_again_again')
lst_pdfs = [element for element in os.listdir() if element.endswith('.pdf')]
pdf_selected = st.selectbox('Choose a pdf',lst_pdfs)

## choose pdf
with open(pdf_selected, "rb") as f:
    pdf = pdftotext.PDF(f)
full_text = "\n\n".join(pdf)
full_text = full_text.replace("\n",' ').lower()
full_text = re.split(r'[.] ',full_text)


check_string = st.text_input("enter search term")

search_results = [sentence for sentence in full_text if check_string.lower() in sentence]
st.write(search_results)
