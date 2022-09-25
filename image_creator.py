import os
import random
from dotenv import load_dotenv
from pyunsplash import PyUnsplash
from string import ascii_letters
import textwrap, requests, io
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

from utils import ImageWriter, get_path
from job_getter import get_jobs

dotenv_path = get_path(".env")
load_dotenv(dotenv_path)

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEYS")

def to_dict(image_object): 
    image = dict()
    image['id'] = image_object.id
    image['url'] = image_object.link_download
    return image


def image_graber(number_of_image=1):
    terms = ["job", "travail", "boulot", "work", "freelancer"]
    term = random.choice(terms)

    pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)

    photos = pu.photos(type_='random', count=number_of_image, featured=True, query=term, orientation="landscape")
    
    
    photo_list = [photo for photo in photos.entries]
    image = [to_dict(photo) for photo in photo_list]

    return image


class TextOnImage:
    """ 
        A simple utility class that will allow the writting of the texts(quotes) to the image
        An issue i faced here waas the resizing of the image to fit instagram image standard (1080 x 1080) 
        I achieved to reached a 100,80 % ration on the sizing using the resampling .BICUBIC method
        I also had to darken the image a bit so the text could be more pleasing to read. 
    """

    def __init__(self, image: Image, text ):
        """ 
            The init of this class takes the following:
            image: Image, a pillow image type
            text:dict, the quote we are to write, of type dict as i found it was easier to manipulate  
        """
        
        image.thumbnail((2878, 1618), Image.Resampling.HAMMING)
        
        #dim image by 50%
        enhancer = ImageEnhance.Brightness(image)
        self.image = enhancer.enhance(0.5)

        self.text = text
        self.draw = ImageDraw.Draw(self.image)

    def draw_text(self, scale=.85, color="white"):
        """ 
            The draw_text function takes in as parameter:
            scale: float, Easily scale the text to fit on image where 1 refers to full scale (fit image completely)
            color: str, using Pillow image attribute to set the font color
        """
        font = ImageFont.truetype("MesloLGS-NF-Bold.ttf",200)
        avg_char_width = sum(font.getlength(char) for char in ascii_letters) / len(ascii_letters)
        max_char_count = int((self.image.size[0] * scale ) /avg_char_width)
        message = textwrap.fill(self.text, max_char_count)
        final_message = message 
        
        position = (self.image.size[0]/2, self.image.size[1]/2)

        self.draw.text(
            xy=(position[0], position[1]),
            text=final_message,
            font=font,
            fill=color,
            anchor="mm"
        )
    

    def show(self):

        self.image.show()
    
    def save_file(self, name):
        final_name = name
        final = ImageWriter(final_name, self.image)
        final.write()


def create_image(text, show: bool =False, save: bool =True):
    image_dict = image_graber()
    
    file_name = image_dict[0]['id']
    img_page = requests.get(image_dict[0]['url']).content
    img = Image.open(io.BytesIO(img_page))
    

    # file_name = "test2"
    # img = Image.open(get_path("moscou.jpg"))

    job_title = text
    image = TextOnImage(img, job_title)
    image.draw_text()

    if show:
        image.show()
    
    if save:
        image.save_file(file_name)

if __name__ == "__main__":
    title = "Avis de recrutement: 01 commercial(e) chevronn\u00e9(e)"
    create_image(title, show=True)
