# from flask import Flask, request, jsonify
# from PyPDF2 import PdfReader
# from utils.Embed import Embeding_DB
# import google.generativeai as genai
# import os

# # Create a Flask app instance
# app = Flask(__name__)

# @app.route("/embed_save_db", methods=['POST'])
# def connect_database():
#     if 'pdf_file' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     pdf_file = request.files['pdf_file']
#     if pdf_file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     # Extract text from the uploaded PDF file
#     pdf_reader = PdfReader(pdf_file)
#     chunk_data = []
    
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             chunk_data.append(page_text)

#     # Create an embedding object and save to Pinecone
#     obj = Embeding_DB(index_name="triluxo", api_key=os.getenv("PINECONE"), filename="output.txt", chunk_data=chunk_data)
#     print("created the object >>>>>>>>>>>>>>>")
#     global retriever
#     retriever = obj.Embed_Save()
    
#     return jsonify({"done": "Embedding and storing in PineconeDB"})


# @app.route("/get_response", methods=['POST'])
# def get_chat():
#     if retriever is None:
#         return jsonify({"error": "No embedding vector space found"}), 400

#     # Get the user query from the request body
#     data = request.get_json()
#     if 'query' not in data:
#         return jsonify({"error": "No query provided"}), 400

#     question = data['query']
    
#     # Generate response using the Gemini API (Replace with actual API call)
#     # Here you should send the question and any necessary context to the Gemini API
#     response = generate_response_with_gemini_api(question)  # Implement this function to call Gemini API
    
#     return jsonify({"content": f">>. {response} <<"})

# def generate_response_with_gemini_api(query):
#     # This function should implement the actual API call to the Gemini API.
#     # You need to replace this with your actual implementation.
#     # Example placeholder response
#     return f"This is a placeholder response for your query: {query}"

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
import streamlit as st
import requests



from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#model setup

model = genai.GenerativeModel('gemini-pro')



def app():
    st.title("PDF Reader with Embedding")
    
    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # Here you would handle the PDF processing and chunking
        # This is a placeholder for your actual chunking logic
        chunk_data = ["This is chunk 1", "This is chunk 2"]  # Replace with actual chunks
        
        # Send chunks to Flask API
        response = requests.post('http://localhost:5000/embed_save_db', json={"chunk_data": chunk_data})
        
        if response.status_code == 200:
            st.success(response.json().get("done"))
        else:
            st.error(response.json().get("error"))

        # User input for querying
        user_query = st.text_input("Ask a question:")
        
        if st.button("Submit"):
            # Send user query to Flask API
            query_response = requests.post('http://localhost:5000/get_response', json={"query": user_query})
            # print(user_query," sadgasdgasd -----> ",query_response.json().get("content"))
            
            #rules 
            rules = """
            1) you cannot answer any question that is irrelavent to the given context
            2)answer in simple and effective manner
            3) if the question is beyound the context, just reply with text as i do not have any specific information on that
            """

            context_content = query_response.json().get("content", "")
            user_query_clean = user_query.strip()  # Remove any leading/trailing spaces
            print(user_query_clean," vivek>>>>", context_content)
            if not context_content:
                # Handle the case where no relevant content is found
                response = "I do not have any specific information on that."
            else:
                # Use the content and user query in a well-formatted way
                # response = model.generate_content(
                #     f"You are a smart AI who has to answer the question: '{user_query_clean}' using the following context: '{context_content}' while following the rules '{rules}'"
                # )
                response = model.generate_content(f"answer the query, query = {user_query_clean} with refrance to the context, context = {context_content}")



            if query_response.status_code == 200:
                st.write(query_response.json().get("content"))
            else:
                st.error(query_response.json().get("error"))

if __name__ == "__main__":
    app()
