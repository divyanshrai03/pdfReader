from utils.extractText import TextExtractor
from utils.generate_store_embeddings import Embeding_DB
from flask import Flask, request, jsonify
from flask import Flask, jsonify
from utils.Log import logger
import os


# Create a Flask app instance
app = Flask(__name__)

@app.route('/', methods=['GET'])
def greet():
    return jsonify({"hellow":f"api is running"})

# Define the route /run
@app.route('/donwload_save', methods=['GET'])
def run():
    data = request.get_json()
    
    # Get the 'url' key from the JSON data
    url = data.get('url') if data else None
    output_file = data.get("output_file") if data else None
    
    # Check if a URL was provided
    if url:
        text = TextExtractor(url,output_file)
        logger.info(">>>>>> Created TextExtractor Object <<<<<<")
        c = text.extract_entire_content()
        logger.info(">>>>>> Compleated TextExtractor Process <<<<<<")
    else:
        logger.error("Url does not exist")
    return jsonify({"done":"build_chat"})
    
@app.route("/embed_save_db", methods=['GET'])
def connect_database():
    obj =Embeding_DB(index_name="triluxo", api_key=os.getenv("PINECONE"),filename="output.txt" )
    print("created the object >>>>>>>>>>>>>>>")
    global retriver
    retriver = obj.Embed_Save()
    return jsonify({"done":"Emeding and storing in pineconeDB"})

@app.route("/get_response", methods=['GET'])
def getChat():
    data = request.get_json()
    question = data.get("question")
    if retriver:
        content = retriver.invoke(question)
    else:
        return jsonify({"error":"No build for Embeding vector space found"})
    return jsonify({"content":f">>. {content} <<"})


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)