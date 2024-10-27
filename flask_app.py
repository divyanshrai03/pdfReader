# import streamlit as st
# from dotenv import load_dotenv
# import pickle
# import os
# from PyPDF2 import PdfReader
# from streamlit_extras.add_vertical_space import add_vertical_space
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS

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
#             chunk_size=500,
#             chunk_overlap=100,
#             length_function=len
#         )
#         chunks = text_splitter.split_text(text=text)
#         st.write(chunks)
#         # Generate or load embeddings
#         store_name = pdf.name[:-4]  # Remove .pdf extension

#     #         if os.path.exists(f"{store_name}.pkl"):
#     #             with open(f"{store_name}.pkl", "rb") as f:
#     #                 VectorStore = pickle.load(f)
#     #             st.success('Embeddings loaded from file.')
#     #         else:
#     #             # Ensure the OpenAI API key is setx
#     #             if not os.getenv("OPENAI_API_KEY"):
#     #                 st.error("OpenAI API key not found. Please add it to your .env file.")
#     #                 return
                
#     #             # Generate embeddings
#     #             embeddings = OpenAIEmbeddings()
#     #             VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
                
#     #             # Save embeddings to file
#     #             with open(f"{store_name}.pkl", "wb") as f:
#     #                 pickle.dump(VectorStore, f)
#     #             st.success(f"Embeddings generated and saved as {store_name}.pkl")

#     #         # Ask a question
#     #         query = st.text_input("Ask a question about your PDF:")
#     #         st.write("You asked:", query)
#     #             # Add logic to handle the query (e.g., searching within VectorStore)

#     #     except Exception as e:
#     #         st.error(f"An error occurred: {e}")
#     # else:
#     #     st.write("Please upload a PDF file.")

 

#     # # Input fields
#     # url = st.text_input("Enter URL:")
#     # output_file = st.text_input("Enter Output File Name:")
#     api_endpoint = "http://127.0.0.1:5000/"
    

#     # # Button to send data to the 'run' endpoint
#     # if st.button("Download And Save"):
#     #     if url and output_file and api_endpoint:
#     #         # Prepare JSON data
#     #         data = {
#     #             "url": url,
#     #             "output_file": output_file
#     #         }

#     #         # Send POST request to `run` API endpoint
#     #         try:
#     #             response = requests.get(api_endpoint+"donwload_save", json=data)
                
#     #             if response.status_code == 200:
#     #                 st.success("Data sent to `run` endpoint successfully!")
#     #                 st.json(response.json())  # Display API response if available
#     #             else:
#     #                 st.error(f"Failed to send data. Status code: {response.status_code}")
#     #                 st.write(response.text)
#     #         except Exception as e:
#     #             st.error(f"An error occurred: {e}")
#     #     else:
#     #         st.warning("Please enter URL, Output File Name, and API Endpoint for `run`.")


#     # index_name = st.text_input("Enter Index Name:")

#     # # Button to send data to the 'embed' endpoint
#     # if st.button("Send Data to Embed "):
#     #     if url and output_file and index_name and api_endpoint:
#     #         # Prepare JSON data
#     #         data = {
#     #             "index_name": index_name
#     #         }

#     #         # Send POST request to `embed` API endpoint
#     #         try:
#     #             response = requests.get(api_endpoint+"embed_save_db", json=data)
                
#     #             if response.status_code == 200:
#     #                 st.success("Data sent to `embed` endpoint successfully!")
#     #                 st.json(response.json())  # Display API response if available
#     #             else:
#     #                 st.error(f"Failed to send data to `embed`. Status code: {response.status_code}")
#     #                 st.write(response.text)
#     #         except Exception as e:
#     #             st.error(f"An error occurred: {e}")
#     #     else:
#     #         st.warning("Please enter URL, Output File Name, Index Name, and API Endpoint for `embed`.")


#     # chat = st.text_input("Enter Chat")

#     # if st.button("Chat "):
#     #     if url and output_file and index_name and api_endpoint:
#     #         # Prepare JSON data
#     #         data = {
#     #             "question": chat
#     #         }
#     #         try:
#     #             response = requests.get(api_endpoint+"get_response", json=data)
                
#     #             if response.status_code == 200:
#     #                 st.success("Data sent to `embed` endpoint successfully!")
#     #                 st.json(response.json())  # Display API response if available
#     #             else:
#     #                 st.error(f"Failed to send data to `embed`. Status code: {response.status_code}")
#     #                 st.write(response.text)
#     #         except Exception as e:
#     #             st.error(f"An error occurred: {e}")
#     #     else:
#     #         st.warning("Please enter URL, Output File Name, Index Name, and API Endpoint for `embed`.")


# if __name__ == '__main__':
#     app()
from flask import Flask, jsonify, request
import os
from utils.Embed import Embeding_DB
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize global variables
retriver = None
chunk_data = []  # Placeholder for chunk data

@app.route("/embed_save_db", methods=['POST'])
def connect_database():
    global retriver, chunk_data  # Declare them as global

    # Get chunk data from the incoming request
    chunk_data = request.json.get('chunk_data', [])
    
    # Check if chunk_data is provided
    if not chunk_data:
        return jsonify({"error": "No chunk data provided."}), 400

    # Create embedding database object
    obj = Embeding_DB(index_name="triluxo", api_key=os.getenv("PINECONE"), filename="output.txt", chunk_data=chunk_data)
    retriver = obj.Embed_Save()  # Store the retriever object globally

    return jsonify({"done": "Embedding and storing in PineconeDB"})


@app.route("/get_response", methods=['POST'])
def getChat():
    global retriver  # Use global retriver

    # Get the user query from the incoming request
    question = request.json.get('query', '')
    
    # Check if retriver is initialized
    if retriver:
        content = retriver.invoke(question)
    else:
        return jsonify({"error": "No build for embedding vector space found."}), 400
        
    return jsonify({"content": f">>. {content} <<"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
