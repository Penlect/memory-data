
import os
import shutil
from PIL import Image

root = r'/home/penlect/Downloads/cfd/CFD Version 2.0.3/CFD 2.0.3 Images'


def copy_images():
    for path, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.jpg'):
                if file.split('-')[-1] == 'N.jpg':
                    fullfile = os.path.join(path, file)
                    gender = file[5]
                    shutil.copy(fullfile, f'cfd_images/{gender}')


def get_images():
    for path, dirs, files in os.walk('cfd_images'):
        for file in files:
            if file.endswith('.jpg'):
                fullpath = os.path.join(path, file)
                original = Image.open(fullpath)
                width, height = original.size
                diff = (width - height)//2
                left =  diff
                top = 0
                right = width - diff
                bottom = height
                new = original.crop((left, top, right, bottom))
                new.save(fullpath)

# copy_images()
# get_images()
