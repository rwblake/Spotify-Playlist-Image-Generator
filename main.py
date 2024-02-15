

import os
import math
from PIL import Image
import imagehash
import argparse
from pathlib import Path
import random


import ordering
import average_color
import generate_mosaic
import pull_images


def filter_duplicates(paths):
	"""Return image paths for images that are not identical. Using imagehash to check for image similarity."""
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
		                help="Spotify playlist URL, or local folder path. URLs start with \'https://open.spotify.com/playlist/\'.")
	parser.add_argument('-r', '--reference_image', type=str,
		                help="Path to reference image. Must be square, and NOT transparent. Otherwise assume random ordering.")
	parser.add_argument('-w', '--width', nargs='?', default=WIDTH_UNSPECIFIED, type=int,
		                help="Width of mosaic in images. Default is automatic.")
	parser.add_argument('-d', '--duplicates', action='store_true',
		                help="Allow duplicate images in mosaic.")
	parser.add_argument('-f', '--force_download', action='store_true',
		                help="Download images, even if folder already exists.")
	return parser.parse_args()


def main():
	# get command line arguments
	args = get_arguments()

	# get_playlist name and cd into relevent folder
	if Path(args.playlist_URL).is_dir():
		playlist_name = args.playlist_URL
	else:
		playlist_name = pull_images.playlist_name(args.playlist_URL)
	if not Path(playlist_name).is_dir():
		os.mkdir(playlist_name)
	os.chdir(playlist_name)

	# pull images if required
	if not Path('images').is_dir():
		os.mkdir('images')
		os.chdir('images')
		pull_images.pull_images(args.playlist_URL)
	elif args.force_download:
		os.chdir('images')
		pull_images.pull_images(args.playlist_URL)
	else:
		os.chdir('images')

	# get paths to all images
	image_paths = os.listdir(".")
	image_paths = filter_duplicates(image_paths)

	# set correct mosaic width for number of images found
	max_width = math.floor(math.sqrt(len(image_paths)))
	if args.width == MAXIMUM_WIDTH:
		args.width = max_width
	# check if there are enough images to create the mosaic
	if not args.duplicates and args.width != WIDTH_UNSPECIFIED and len(image_paths) < args.width**2:
		raise Exception(f"Not enough images to create mosaic of width {args.width}. Maximum width is {max_width} for {len(image_paths)} images.")

	if args.reference_image is not None:
		# calculate average colour for each image
		averages = average_color.get_average_colors(image_paths)
		print(f"Available images: {len(averages)}")

		# calculate positions (ordering) for images in mosaic
		if args.width == WIDTH_UNSPECIFIED:
			# try all widths from 2X2 to max_widthXmax_width
			orders = []
			for i in range(max_width, 1, -1):
				order = ordering.ordering("../../"+args.reference_image, i, averages, args.duplicates)
				orders.append(order)
				print(f"Width: {i:03}\tError: {order[1]}")
			# choose ordering with minimum error
			order = min(orders, key=lambda x:x[1])[0]
			args.width = math.floor(math.sqrt(len(order)))  # set new width
		else:
			order = ordering.ordering("../../"+args.reference_image, args.width, averages, args.duplicates)[0]
		print(f"Using width {args.width} with {len(order)} images.")
	else:
		if args.width == WIDTH_UNSPECIFIED:
			args.width = max_width
		random.shuffle(image_paths)
		order = image_paths[:max_width**2]
		args.reference_image = 'random'

	# generate mosaic
	image = generate_mosaic.generate_mosaic(1600, args.width, order)
	image.save(f"{Path(args.reference_image).stem}_mosaic.png")
	image.show()


if __name__ == "__main__":
	main()
