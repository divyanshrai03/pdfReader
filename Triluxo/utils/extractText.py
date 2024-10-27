import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter
from utils.Log import logger


class TextExtractor:
    def __init__(self, url, output_file="output" ):
        self.url  = url
        self.output_file = output_file
    def extract_entire_content(self):
        """
        Returns the extractd text as a text file
        Args:
            None
        Reutrns:
            None
        """

        try:
            # Send a GET request to the website
            logger.info("-- Getting response using url --")
            response = requests.get(self.url)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the content of the website using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get the entire text content from the website
                entire_content = soup.get_text(separator='\n')  # separator adds new lines for readability
                
                # Save the extracted content to a text file
                with open(self.output_file, 'w', encoding='utf-8') as file:
                    file.write(entire_content)
                
                logger.info(f"---- Entire content extracted and saved to {self.output_file} ----")
            else:
                logger.info(f"---- Failed to retrieve the webpage. Status code: {response.status_code} ----")
        except Exception as e:
            logger.error(f"----An error occurred: {e}----")
        return entire_content
if __name__ == "__main__":
    pass