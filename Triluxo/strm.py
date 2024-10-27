import streamlit as st
import requests
import json

# Streamlit app
def app():
    st.title("URL, Output File, and Index Name JSON Sender")

    # Input fields
    url = st.text_input("Enter URL:")
    output_file = st.text_input("Enter Output File Name:")
    api_endpoint = "http://127.0.0.1:5000/"
    

    # Button to send data to the 'run' endpoint
    if st.button("Download And Save"):
        if url and output_file and api_endpoint:
            # Prepare JSON data
            data = {
                "url": url,
                "output_file": output_file
            }

            # Send POST request to `run` API endpoint
            try:
                response = requests.get(api_endpoint+"donwload_save", json=data)
                
                if response.status_code == 200:
                    st.success("Data sent to `run` endpoint successfully!")
                    st.json(response.json())  # Display API response if available
                else:
                    st.error(f"Failed to send data. Status code: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter URL, Output File Name, and API Endpoint for `run`.")


    index_name = st.text_input("Enter Index Name:")

    # Button to send data to the 'embed' endpoint
    if st.button("Send Data to Embed "):
        if url and output_file and index_name and api_endpoint:
            # Prepare JSON data
            data = {
                "index_name": index_name
            }

            # Send POST request to `embed` API endpoint
            try:
                response = requests.get(api_endpoint+"embed_save_db", json=data)
                
                if response.status_code == 200:
                    st.success("Data sent to `embed` endpoint successfully!")
                    st.json(response.json())  # Display API response if available
                else:
                    st.error(f"Failed to send data to `embed`. Status code: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter URL, Output File Name, Index Name, and API Endpoint for `embed`.")


    chat = st.text_input("Enter Chat")

    if st.button("Chat "):
        if url and output_file and index_name and api_endpoint:
            # Prepare JSON data
            data = {
                "question": chat
            }
            try:
                response = requests.get(api_endpoint+"get_response", json=data)
                
                if response.status_code == 200:
                    st.success("Data sent to `embed` endpoint successfully!")
                    st.json(response.json())  # Display API response if available
                else:
                    st.error(f"Failed to send data to `embed`. Status code: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter URL, Output File Name, Index Name, and API Endpoint for `embed`.")


if __name__ == '__main__':
    app()