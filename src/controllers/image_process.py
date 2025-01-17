from flask import Blueprint, request, jsonify
from src.utils import upload

class ImageProcessController:
    def __init__(self, stitching_service):
        self.stitching_service = stitching_service

    def register_routes(self, app):
        image_blueprint = Blueprint('image_process', __name__)

        @image_blueprint.route('/stitch/<public_id>', methods=['POST'])
        def stich_image(public_id):
            files = request.files.getlist('images')
            images = []
            for file in files:
                images.append(file.read())

            self.stitching_service.read_image(images)
            stitched_image = self.stitching_service.stich_images()

            if stitched_image is not None:
                upload_result = upload.upload_image(stitched_image, folder='stitched_images', public_id=public_id)
                if upload_result is not None:
                    return jsonify({'url': upload_result['url']})
            return jsonify({'error': 'Stitching ERROR'}), 500
            
        app.register_blueprint(image_blueprint)