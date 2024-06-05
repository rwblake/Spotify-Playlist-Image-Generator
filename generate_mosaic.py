

import os
import math
from PIL import Image
from tqdm import tqdm


def generate_mosaic(width, images_wide, image_paths):
	image = Image.new(mode="RGB", size=(width, width))
	tile_width = width // images_wide

	for i, path in tqdm(enumerate(image_paths), total=len(image_paths)):
		tmp_image = Image.open(path)
		tmp_image = tmp_image.resize((tile_width, tile_width))
		image.paste(tmp_image, (i % images_wide * tile_width, i // images_wide * tile_width))

	os.chdir("..")
	return image


def main():
	import sys
	if len(sys.argv) < 2:
		print(f"Expected usage: {sys.argv[0]} playlist_directory width_in_pixels number_of_images_wide")
	directory_name = sys.argv[1]
	if len(sys.argv) >= 3:
		width = sys.argv[2]
	else:
		width = 1600

	os.chdir(sys.argv[1])
	os.chdir("images")
	if len(sys.argv) >= 4:
		images_wide = sys.argv[3]
	else:
		images_wide = math.floor(math.sqrt(len(os.listdir('.'))))
	image_paths = os.listdir(".")[:images_wide**2]

	output = generate_mosaic(width, images_wide, image_paths)
	output.show()


if __name__ == "__main__":
	main()