from PIL import Image, ExifTags, JpegImagePlugin
import os
import subprocess

folder_path = '/path/to/image/folder/'
quality = 90
convert_png_to_jpeg = True
max_width = 800
png_crush = False
skip_small_files = True
file_size_limit_mb = 2  # in MB

def resize_image(image, max_width):
    if image.width > max_width:
        new_height = int((max_width / image.width) * image.height)
        return image.resize((max_width, new_height), Image.LANCZOS)
    return image

def get_exif_data(image):
    if hasattr(image, '_getexif'):
        return image._getexif()
    return None

def save_with_metadata(image, file_path, format=None, **kwargs):
    exif_data = None
    if format == 'JPEG':
        exif = get_exif_data(image)
        if exif is not None:
            exif_data = JpegImagePlugin.getexif(image)._getexif()

    if exif_data is not None:
        image.save(file_path, format=format, exif=exif_data, **kwargs)
    else:
        image.save(file_path, format=format, **kwargs)

def is_small_file(file_path, size_limit):
    size_limit_bytes = size_limit * 1024 * 1024
    return os.path.getsize(file_path) <= size_limit_bytes

processed_count = 0
skip_messages = ["\n"]

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    file_extension = file_name.lower().endswith(('.png', '.jpg', '.jpeg'))

    if file_extension:
        try:
            image = Image.open(file_path)
        except (Image.UnidentifiedImageError, OSError):
            continue

        if skip_small_files and is_small_file(file_path, file_size_limit_mb) and image.width <= max_width:
            skip_messages.append(f"Skipping small file ({file_size_limit_mb}MB or less and width <= {max_width}px): {file_name}")
        else:
            image = resize_image(image, max_width)

            new_file_path = file_path.rsplit('.', 1)[0] + '.png'
            if file_name.lower().endswith('.png'):
                if png_crush:
                    subprocess.run(['pngcrush', '-ow', file_path])

                image.save(new_file_path, format='PNG', optimize=True)
                if file_path != new_file_path:
                    os.remove(file_path)
            elif file_name.lower().endswith(('.jpg', '.jpeg')) and convert_png_to_jpeg:
                image = image.convert('RGB')
                save_with_metadata(image, new_file_path, format='PNG', optimize=True)
                os.remove(file_path)

        processed_count += 1
        print(".", end='', flush=True)

for skip_message in skip_messages:
    print(skip_message)

print(f"\n")
print(f"Processed {processed_count} images.")
print(f"Images processed and quality set to {quality}%.")
print(f" * Image width set to {max_width}px.")
print(f" * Skip all files {file_size_limit_mb}MB or smaller.")
print(f" * Skip all files with width <= {max_width}px.")
