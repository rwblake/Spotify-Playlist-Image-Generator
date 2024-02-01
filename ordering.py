

from PIL import Image
import random


def distance(c1, c2):
	r1, g1, b1 = c1
	r2, g2, b2 = c2
	return (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2


def ordering(reference_image_path, images_wide, averages):
	reference_image = Image.open(reference_image_path)
	if reference_image.size[0] != reference_image.size[1]:
		raise Exception("Reference image not square.")
	reference_image = reference_image.resize((images_wide, images_wide))

	ordering = [None for i in range(images_wide**2)]  # populate array
	free_pixels = [i for i in range(images_wide**2)]
	random.shuffle(free_pixels)  # ensure that no pixel is preferentially chosen

	for i, pixel_number in enumerate(free_pixels):
		reference_pixel = reference_image.getpixel((pixel_number % images_wide, pixel_number // images_wide))
		distances = []

		for (path, average) in averages:
			distances.append(((path, average), distance(average, reference_pixel)))

		(path, average), d = min(distances, key=lambda x: x[1])
		averages.remove((path, average))
		ordering[pixel_number] = path

	return ordering



def main():
	import sys
	import math
	import os
	import average_color
	if len(sys.argv) < 2:
		raise Exception(f"Invalid arguments, use: {sys.argv[0]} playlist_name reference_image images_wide")
	if len(sys.argv) >= 2:
		playlist = sys.argv[1]
	if len(sys.argv) >= 3:
		reference = sys.argv[2]
	else:
		reference = "reference.png"  # default

	os.chdir(playlist)
	os.chdir("images")
	if len(sys.argv) >= 4:
		images_wide = sys.argv[3]
	else:
		images_wide = math.floor(math.sqrt(len(os.listdir('.'))))  # default is maximum size

	averages = average_color.get_average_colors(os.listdir('.'))[:images_wide**2]
	os.chdir("..")
	os.chdir("..")
	print(ordering(reference, images_wide, averages))


if __name__ == "__main__":
	main()