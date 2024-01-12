# image-redux
Simple Python script to reduce the file size of images.
=======

# Image Redux

Image Redux is a Python script for processing and optimizing images in a specified folder. It resizes images to a maximum width, converts PNG files to JPEG (optional), and can skip small files based on size and width.

## Usage

1. Clone this repository to your local machine or download the script `redux.py`.

2. Navigate to the folder containing the script in your terminal.

3. Install the required Python libraries if you haven't already:

   ```
   # Using pip3
   pip3 install pillow
   pip3 install thumbor-plugins-pngcrush
   ```

   ```
   # Debain
   sudo apt install python3-pillow
   sudo apt install pngcrush
   ```

4. Run the script using the following command:

   ```
   python3 redux.py
   ```

## Configuration

You can configure the script by modifying the following variables in `redux.py`:

- `folder_path`: The path to the folder containing the images you want to process.
- `quality`: The quality of the output images (0-100).
- `convert_png_to_jpeg`: Set to `True` if you want to convert PNG files to JPEG and then back to PNG for maximum optimization.
- `max_width`: The maximum width for resized images.
- `png_crush`: Set to `True` if you want to optimize PNG files using `pngcrush`.
- `skip_small_files`: Set to `True` to skip images that are smaller than a specified size.
- `file_size_limit_mb`: The file size limit in megabytes for skipping small files.

## Output

The script will process the images in the specified folder and **overwrite** the old file. After processing, it will provide a summary of the number of images processed, the image quality, maximum width, and skip criteria.

If any images cannot be identified or processed, they will be skipped, and a list of skipped images will be displayed in the summary.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.