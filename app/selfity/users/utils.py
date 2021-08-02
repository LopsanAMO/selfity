import json
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class CustomValidationError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail=None, field=None, status_code=None, message=None):
        if status_code is not None:
            self.status_code = status_code
        if isinstance(detail, dict):
            self.detail = detail
        else:
            if detail is not None:
                self.detail = {'field': field, 'detail': force_text(detail)}
            else:
                self.detail = {'detail': force_text(self.default_detail)}


def make_thumbnail(dst_image_field, src_image_field, size, name_suffix, sep='_'):
    image = Image.open(src_image_field)
    image.thumbnail(size, Image.ANTIALIAS)
    dst_path, dst_ext = os.path.splitext(src_image_field.name)
    dst_ext = dst_ext.lower()
    dst_fname = dst_path + sep + name_suffix + dst_ext
    if dst_ext in ['.jpg', '.jpeg']:
        filetype = 'JPEG'
    elif dst_ext == '.gif':
        filetype = 'GIF'
    elif dst_ext == '.png':
        filetype = 'PNG'
    else:
        raise RuntimeError('unrecognized file type of "%s"' % dst_ext)

    dst_bytes = BytesIO()
    image.save(dst_bytes, filetype)
    dst_bytes.seek(0)

    dst_image_field.save(dst_fname, ContentFile(dst_bytes.read()), save=False)
    dst_bytes.close()