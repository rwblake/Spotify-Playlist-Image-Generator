
import os
import sys
import math
from PIL import Image
import imagehash


import ordering
import average_color
import generate_mosaic
import pull_images


def filter_duplicates(paths):
	hashes = []
	ret = []
	for path in paths:
		image_hash = imagehash.average_hash(Image.open(path))
		if image_hash in hashes:
			continue
		hashes.append(image_hash)
		ret.append(path)
	return ret


def main():
	if len(sys.argv) != 4:
		print(f"Usage: {sys.argv[0]} playlist_url width reference")
		return

	playlist_name = pull_images.pull_images(sys.argv[1])
	images_wide = int(sys.argv[2])  # how many albums wide the result will be
	reference = sys.argv[3]

	os.chdir(playlist_name)
	os.chdir("images")

	image_paths = os.listdir(".")
	image_paths = filter_duplicates(image_paths)

	averages = average_color.get_average_colors(image_paths)
	print(len(averages))
	
	if images_wide == 0:
		images_wide = math.floor(math.sqrt(len(image_paths)))
		orders = [ordering.ordering("../../"+reference, i, averages) for i in range(images_wide, 1, -1)]
		for order in orders:
			print(len(order[0]), order[1])
		order = min(orders, key=lambda x:x[1])[0]
	else:
		order = ordering.ordering("../../"+reference, images_wide, averages)[0]
	print(len(order))
	images_wide = math.floor(math.sqrt(len(order)))

	image = generate_mosaic.generate_mosaic(1600, images_wide, order)
	image.show()


if __name__ == "__main__":
	main()
