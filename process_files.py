
import json
import os
from pathlib import Path
import hashlib
from PIL import Image
import face_recognition as fr



def files():
    """Yield files with image_link duplicates removed"""
    seen = set()
    for log_file in Path('./img/scraping/logs').iterdir():
        with open(log_file, 'r') as f:
            data = json.load(f)
            for item in data:
                if item['filename'].strip():
                    if item['image_link'] not in seen:
                        seen.add(item['image_link'])
                        folder = log_file.stem
                        yield folder, item['filename']


def md5(fname):
    """Compute checksum of file"""
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def rename_gender_md5(image_folder, gender, dry_run=False):
    """Rename images to gender-checksum filename for face-images."""
    image_folder = Path(image_folder)
    for file in image_folder.iterdir():
        if file.is_file() and file.suffix.lower() in {'.jpg', '.png'}:
            checksum = md5(file)
            if gender == 'men':
                prefix = 1
            elif gender == 'women':
                prefix = 0
            else:
                raise ValueError(f'Unknown gender: {gender}')
            new_filename = f'{prefix}-{checksum}{file.suffix}'
            print(new_filename, '<-', file.name)
            if not dry_run:
                file.rename(file.with_name(new_filename))


def images():
    duplicates = dict()
    download = Path('./img/scraping/download')
    for folder, file in files():
        img = download / folder / file
        try:
            if img.exists():
                s = md5(img)
                if s not in duplicates:
                    yield img
                duplicates.setdefault(s, list()).append(img)
        except OSError:
            pass
    dup_count = 0
    for s, imgs in duplicates.items():
        for file in imgs[1:]:
            file.unlink()
            dup_count += 1
    print(f'Deleted {dup_count} duplicated files.')


def process():
    index = 0
    with open('log.txt', 'w') as log:
        for img in images():
            #print(img)
            try:
                image = fr.load_image_file(img)
            except OSError as err:
                print(err)
                continue
            # Image.fromarray(image).show()
            face_locations = fr.face_locations(image)
            for face_location in face_locations:
                top, right, bottom, left = face_location
                #print(f'Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}')
                dx = right - left
                dy = bottom - top
                # Make image square
                if dx <= dy:
                    padding = (dy - dx)//2
                    right += padding
                    left -= padding
                else:
                    padding = (dx - dy)//2
                    bottom += padding
                    top += padding
                s = max(dx, dy)
                left -= int(s*0.5)
                right += int(s*0.5)
                bottom += int(s*0.3)
                top -= int(s*0.7)
                #print(top, left, bottom, right)
                if left < 0:
                    right -= left
                    left = 0
                if top < 0:
                    bottom -= top
                    top = 0

                # You can access the actual face itself like this:
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                # pil_image.show()
                with open(f'output/{index:05}.jpg', 'wb') as f:
                    pil_image.save(f)
                    log.write(f'{index:05};{img.name}\n')
                    index += 1


if __name__ == '__main__':
    prev = -10
    for file in os.listdir('output'):
        n = int(file.split('.')[0])
        if n != prev + 1:
            print(n)
        prev = n
