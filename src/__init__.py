from flask import Flask
from .config import Config
from src.controllers import image_process
from src.services import stitching_image
app = Flask(__name__)

app.config.from_object(Config)

stitching_service = stitching_image.StichingImage()
image_process_controller = image_process.ImageProcessController(stitching_service)

image_process_controller.register_routes(app)