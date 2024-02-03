
import os
import math
from PIL import Image
import imagehash
import argparse


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


WIDTH_UNSPECIFIED = 0
MAXIMUM_WIDTH = -1


def get_arguments():
	parser = argparse.ArgumentParser(description="Create a mosaic playlist cover from a reference image.")
	parser.add_argument('playlist_URL', type=str,
		                help="Spotify playlist URL. Starts with \'https://open.spotify.com/playlist/\'.")
	parser.add_argument('reference_image', type=str,
		                help="Path to reference image. Must be square, and NOT transparent.")
	parser.add_argument('-w', '--width', nargs='?', default=WIDTH_UNSPECIFIED, const=MAXIMUM_WIDTH, type=int,
		                help="Width of mosaic in images. Default is automatic. No value picks maximum possible width.")
	parser.add_argument('-d', '--duplicates', action='store_true',
		                help="Allow duplicate images in mosaic.")
	return parser.parse_args()


def main():
	args = get_arguments()

	playlist_name = pull_images.pull_images(args.playlist_URL)

	os.chdir(playlist_name)
	os.chdir("images")

	image_paths = os.listdir(".")
	image_paths = filter_duplicates(image_paths)

	averages = average_color.get_average_colors(image_paths)
	print(len(averages))

	max_width = math.floor(math.sqrt(len(image_paths)))
	if args.width == MAXIMUM_WIDTH:
		args.width = max_width

	if not args.duplicates and args.width != WIDTH_UNSPECIFIED and len(image_paths) < args.width**2:
		raise Exception(f"Not enough images to create mosaic of width {args.width}. Maximum width is {max_width} for {len(image_paths)} images.")
	
	if args.width == WIDTH_UNSPECIFIED:
		orders = []
		for i in range(max_width, 1, -1):
			order = ordering.ordering("../../"+args.reference_image, i, averages, args.duplicates)
			orders.append(order)
			print(f"Width: {i:03}\tError: {order[1]}")
		order = min(orders, key=lambda x:x[1])[0]
	else:
		order = ordering.ordering("../../"+args.reference_image, args.width, averages, args.duplicates)[0]
	print(len(order))

	args.width = math.floor(math.sqrt(len(order)))
	image = generate_mosaic.generate_mosaic(1600, args.width, order)
	image.show()


if __name__ == "__main__":
	main()
