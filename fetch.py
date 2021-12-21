import requests
import os
from typing import Union

def fetch_image(url: str, fetch_name: str) -> Union[str, None]:
    """ Fetches an image from a url, supports JPG and PNG """
    try:
        valid_image_types = ("image/jpeg", "image/jpg", "image/png")
        response = requests.get(url)
        content_type = response.headers.get("Content-Type")
        is_image =  content_type in valid_image_types
        
        if not is_image:
           print("Url is not valid.")
           return None
    
        caller_path = os.getcwd()
        file_path = os.path.join(caller_path, fetch_name + ".png")
        
        # Create file
        with open(file_path, "wb+") as file:
            file.write(response.content)

        return file_path
    except requests.exceptions.ConnectionError:
        print("No internet connection")
