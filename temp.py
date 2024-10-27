# import streamlit as st
# from dotenv import load_dotenv
# import os
# from PyPDF2 import PdfReader
# from streamlit_extras.add_vertical_space import add_vertical_space
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # Load environment variables
# load_dotenv()

# # Sidebar contents
# with st.sidebar:
#     st.title("PDF Chat App")
#     st.markdown(""" 
#     This app allows you to chat with your PDF.
#     """)
#     add_vertical_space(5)
#     st.write("Made with ❤️ by Divyansh Rai (https://github.com/divyanshrai003)")    

# # Streamlit app
# def app():
    
#     st.title("Chat with your PDF📚")

#     # Upload a PDF file
#     pdf = st.file_uploader("Upload your PDF file", type="pdf")

#     if pdf is not None:
#         # Display the file name
#         st.write(f"Uploaded file: {pdf.name}")

#         # Process the PDF
#         pdf_reader = PdfReader(pdf)
#         text = ""
#         for page in pdf_reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text
#             else:
#                 st.warning("Some pages may not be readable.")
        
#         if not text:
#             st.error("Could not extract text from the PDF.")
#             return

#         # Split text into chunks
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200,
#             length_function=len
#         )
#         chunks = text_splitter.split_text(text=text)

#         # Display the chunks as a list
#         st.write("Extracted Text Chunks (as a list):")
#         st.write(chunks)  # This will show the chunks in a list format
        
#         # Optional: Display type of the 'chunks' variable to verify it is a list
#         st.write(f"Type of chunks: {type(chunks)}")  # Should output <class 'list'>
        
#         # You can further process this list of chunks for embeddings or other purposes

# if __name__ == "__main__":
#     app()


from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#model setup

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Write a story about vit chennai in 50 words")
print(response.text)

