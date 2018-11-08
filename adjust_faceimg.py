
import os
import shutil
import hashlib
import itertools
from pathlib import Path
from PIL import Image

root = r'/home/penlect/src/memory-data/_em2018_originals'
output = r'/home/penlect/src/stdmemory/stdmemo/static/img/profile-images/_em2018'


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_images():
    files = itertools.chain((Path(root) / 'F').iterdir(),
                            (Path(root) / 'M').iterdir())
    for file in files:
        gender = file.parent.name
        print(gender, file.name)
        gender_int = '1' if gender == 'M' else '2'
        original = Image.open(file)
        output_dir = Path(output) / gender
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / (gender_int + '-' + md5(file) + '.jpg')
        width, height = original.size
        print(f'{height/width:.2f}', width, height)

        # Crop
        if width > height:
            diff = (width - height) // 2
            left = diff
            top = 0
            right = width - diff
            bottom = height
            new = original.crop((left, top, right, bottom))
            if height > 600:
                new = new.resize((600, 600), Image.ANTIALIAS)
            new.save(output_file)
        elif width < height:
            new_size = (height, height)
            new = Image.new(original.mode, new_size, color='white')
            new.paste(original, ((height - width)//2, 0))
            if height > 600:
                new = new.resize((600, 600), Image.ANTIALIAS)
            new.save(output_file)
        else:
            new = original
            if height > 600:
                new = new.resize((600, 600), Image.ANTIALIAS)
            new.save(output_file)
        print()


get_images()
