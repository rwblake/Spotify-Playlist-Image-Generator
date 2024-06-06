

import os
import math
from PIL import Image
import imagehash
import argparse
from pathlib import Path
import random
import sys
import subprocess


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


MAXIMUM_WIDTH = -1


def get_arguments():
	parser = argparse.ArgumentParser(description="Create a mosaic playlist cover from a reference image.")
	parser.add_argument('playlist_URL', type=str,
		                help="spotify playlist URL (\'https://open.spotify.com/playlist/...\') OR local folder path")
	parser.add_argument('reference_image', type=str, nargs='?', default=None,
		                help="path to reference image (must be square)")
	parser.add_argument('-w', '--width', type=int,
		                help="width of mosaic in images (default 64x64)")
	parser.add_argument('-n', '--no-duplicates', action='store_false', dest='duplicates',
		                help="only use each image once")
	parser.add_argument('-f', '--force-download', action='store_true', dest='force_download',
		                help="force image re-downloading when playlist has previously been used")
	return parser.parse_args()


def openImage(path):
    imageViewerFromCommandLine = {'linux':'xdg-open',
                                  'win32':'explorer',
                                  'darwin':'open'}[sys.platform]
    subprocess.Popen([imageViewerFromCommandLine, path])


def main():
	# get command line arguments
	args = get_arguments()

	print("1/4 Loading images")
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
	if args.width == MAXIMUM_WIDTH or args.width is None:
		# ensure there is room for all images to be acommodated
		args.width = max_width + 1
	# check if there are enough images to create the mosaic
	if not args.duplicates and len(image_paths) < args.width**2:
		raise Exception(f"Not enough images to create mosaic of width {args.width}. Maximum width is {max_width} for {len(image_paths)} images.")

	print("2/4 Checking for duplicate images")
	if args.reference_image is not None:
		# calculate average colour for each image
		averages = average_color.get_average_colors(image_paths)
		print(f"Available images: {len(averages)}")
		print("3/4 Calculating mosaic layout")
		# calculate positions (ordering) for images in mosaic
		order = ordering.ordering("../../"+args.reference_image, args.width, averages, args.duplicates)[0]
	else:
		order = image_paths

		discrepancy = args.width**2 - len(image_paths)
		if discrepancy > 0:
			order.extend([random.choice(image_paths) for _ in range(discrepancy)])
		
		random.shuffle(order)
		args.reference_image = 'random'

	# generate mosaic
	print("4/4 Saving final mosaic")
	image = generate_mosaic.generate_mosaic(1600, args.width, order)
	image_name = f"{Path(args.reference_image).stem}_mosaic_{args.width}x.png"
	image.save(image_name)
	print("Saved as " + image_name)
	openImage(image_name)


if __name__ == "__main__":
	main()
