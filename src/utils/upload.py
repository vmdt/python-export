from src.config import Config
import cloudinary
import cloudinary.uploader
import cloudinary.api

def upload_image(image, folder=None, public_id=None, over_write=True):
    try:
        upload_options = {
            'folder': folder,
            'public_id': public_id,
            'overwrite': over_write
        }
        upload_options = {k: v for k, v in upload_options.items() if v is not None}
        upload_result = cloudinary.uploader.upload(image, **upload_options)
        return upload_result
    except Exception as e:
        print(e)
        return None
