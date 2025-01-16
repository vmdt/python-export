from flask import Blueprint, request, Response

class ImageProcessController:
    def __init__(self, stitching_service):
        self.stitching_service = stitching_service

    def register_routes(self, app):
        image_blueprint = Blueprint('image_process', __name__)

        @image_blueprint.route('/stitch', methods=['POST'])
        def stich_image():
            files = request.files.getlist('images')
            images = []
            for file in files:
                images.append(file.read())

            self.stitching_service.read_image(images)
            stitched_image = self.stitching_service.stich_images()

            if stitched_image is not None:
                return Response(stitched_image, mimetype='image/jpeg')
            else:
                return Response('Error', status=500)
            
        app.register_blueprint(image_blueprint)