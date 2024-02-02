
import os
import sys
import math
from PIL import Image


import ordering
import average_color
import generate_mosaic
import pull_images


def main():
	if len(sys.argv) != 4:
		print(f"Usage: {sys.argv[0]} playlist_url width reference")
		return

	playlist_name = pull_images.pull_images(sys.argv[1])
	images_wide = int(sys.argv[2])  # how many albums wide the result will be
	reference = sys.argv[3]

	os.chdir(playlist_name)
	os.chdir("images")

	if images_wide == 0:
		images_wide = math.floor(math.sqrt(len(os.listdir('.'))))
	image_paths = os.listdir(".")

	averages = average_color.get_average_colors(image_paths)
	print(len(averages))
	order = ordering.ordering("../../"+reference, images_wide, averages)
	print(len(order))

	image = generate_mosaic.generate_mosaic(1600, images_wide, order)
	image.show()


if __name__ == "__main__":
	main()
