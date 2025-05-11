from flask import Blueprint, request, jsonify
from src.utils import upload
import requests

class ImageProcessController:
    def __init__(self, stitching_service):
        self.stitching_service = stitching_service

    def register_routes(self, app):
        image_blueprint = Blueprint('image_process', __name__)

        @image_blueprint.route('/stitch/<public_id>', methods=['POST'])
        def stich_image(public_id):
            data = request.get_json()

            image_urls = data.get('images', [])
            folder = data.get('folder')
            if not image_urls or not isinstance(image_urls, list):
                return jsonify({'error': 'Invalid or missing images'}), 400

            if not folder:
                return jsonify({'error': 'Missing folder name'}), 400
            
            images = []
            for url in image_urls:
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    images.append(response.content)
                except Exception as e:
                    return jsonify({'error': f'Failed to download image from {url}', 'details': str(e)}), 400


            self.stitching_service.read_image(images)
            stitched_image = self.stitching_service.stich_images()

            if stitched_image is not None:
                upload_result = upload.upload_image(stitched_image, folder=folder, public_id=public_id)
                if upload_result is not None:
                    return jsonify({'url': upload_result['secure_url']})
            return jsonify({'error': 'Stitching ERROR'}), 500
            
        app.register_blueprint(image_blueprint)