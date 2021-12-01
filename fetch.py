import requests
import os
from datetime import datetime
from typing import Union
from config import OUTPUT_FOLDER_NAME

def fetch_image(url: str, output_name: str) -> Union[str, None]:
    """ Fetches an image from a url, supports JPG and PNG """
    try:
        valid_image_types = ("image/jpeg", "image/jpg", "image/png")
        response = requests.get(url)
        content_type = response.headers.get("Content-Type")
        is_image =  content_type in valid_image_types
        
        if not is_image:
           print("Url is not valid.")
           return None
        
        timestamp = str(datetime.now().microsecond)
        file_name = "fetch-tmp-" + timestamp + ".png"
        tmp_path = os.path.abspath(os.path.join(__file__, ".."))
        file_path = os.path.join(tmp_path, file_name)
        
        # Create file
        with open(file_path, "wb+") as file:
            file.write(response.content)

        return file_path
    except requests.exceptions.ConnectionError:
        print("No internet connection")



if __name__ == "__main__":
    url_jpg = "https://imgr.search.brave.com/A40nL8Njwq97vboweikZtGFdyh8tqKF9GlticIWO5Fk/fit/1200/1140/ce/1/aHR0cHM6Ly9zbG92/YWthdGlvbi5jb20v/d3AtY29udGVudC91/cGxvYWRzLzIwMTUv/MTEvSU1HXzQyMTku/anBn"
    url_dog = "https://imgr.search.brave.com/jL4VrT4aAx6mEWlRIGrtAXk-lTpULwQenAh6ColgaEs/fit/1200/1065/ce/1/aHR0cHM6Ly9nZnAt/MmEzdG5wemouc3Rh/Y2twYXRoZG5zLmNv/bS93cC1jb250ZW50/L3VwbG9hZHMvMjAx/OC8wNi9kb2ctYnJl/ZWRzLW9mLWZhbW91/cy1kb2dzLTE2MDB4/MTA2NS5qcGc"
    url_jungle = "https://imgr.search.brave.com/SfmOLP5QMtxKPnb5d3yM4G4-nvpEGTO_vbLgP4178wU/fit/1200/1200/ce/1/aHR0cDovL3d3dy5w/aXhlbHN0YWxrLm5l/dC93cC1jb250ZW50/L3VwbG9hZHMvMjAx/Ni8wNi9KdW5nbGUt/UGljdHVyZXMuanBn"
    invalid_url = "https://search.brave.com/search?q=check+if+bytes+is+an+image+python&source=web"
    fetch_image(url_jungle, "")