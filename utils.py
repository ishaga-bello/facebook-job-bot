import os
from os.path import join
from PIL import Image

def get_path(path_name, file_name=None):
    """
     A simple function that reurns a filepath
     Enter only a file destination or enter folder and a filename
    """
    try:
        if file_name:
            return os.path.join(os.path.dirname(os.path.realpath("__file__")), str(path_name), str(file_name))
        else:
            return os.path.join(os.path.dirname(os.path.realpath("__file__")), str(path_name))
    except FileNotFoundError as e:
        print(e)
    


class ImageWriter:
    """ An image writer class to easily write/ save images to disk 
    It takes a binary(byte) image type"""

    def __init__(self, name, content, location= '.'):
        self.name = name
        self.content = content
        self.location = location

    def write(self):
        
        folder = get_path(self.location)
        
        image_content = self.content

        file_name = self.name + '.jpg'
        write_folder = join(folder, file_name)

        print('writing %s to %s' %(file_name, folder))
        image_content.save(write_folder, format="jpeg")

        print('write successful')

def resize(path):
    
    for img in os.listdir(path):
        if img.endswith("jpg"):
            image = Image.open(get_path(path,img))

            resize_path = get_path("resize")
            new_path = get_path(resize_path, img)
            
            image = image.resize((1080, 1920), Image.Resampling.LANCZOS)
            image.save(new_path, "JPEG", quality=90)

def clean(path):
    try:
        for file in os.listdir(path):
            os.remove(get_path(path, file))
    except FileNotFoundError as e:
        print(e)
    
