import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

class Config:
    PORT = os.getenv("PORT", 5050)
    CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")

    def __init__(self):
        self.init_cloudinary()

    @staticmethod
    def init_cloudinary():
        cloudinary.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET,
        )
