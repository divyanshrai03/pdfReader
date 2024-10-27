import streamlit as st
import requests
import json

# Streamlit app
def app():
    st.title("URL and Output File JSON Sender")

    # Input fields
    url = st.text_input("Enter URL:")
    output_file = st.text_input("Enter Output File Name:")
    api_endpoint = st.text_input("Enter API Endpoint ")

    # Button to send data
    if st.button("Send Data"):
        if url and output_file and api_endpoint:
            # Prepare JSON data
            data = {
                "url": url,
                "output_file": output_file
            }

            # Send POST request to API endpoint
            try:
                response = requests.get(api_endpoint, json=data)
                
                if response.status_code == 200:
                    st.success("Data sent successfully!")
                    st.json(response.json())  # Display API response if available
                else:
                    st.error(f"Failed to send data. Status code: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter both URL, Output File Name, and API Endpoint.")

if __name__ == '__main__':
    app()