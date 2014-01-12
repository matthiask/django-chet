from datetime import datetime
from PIL import Image, ExifTags


def read_shot_on(file):
    img = Image.open(file)

    exif = {
        ExifTags.TAGS.get(k, k): v
        for k, v in img._getexif().items()
    }

    if 'DateTimeOriginal' in exif:
        return datetime.strptime(
            exif['DateTimeOriginal'],
            '%Y:%m:%d %H:%M:%S',
        )

    return None
