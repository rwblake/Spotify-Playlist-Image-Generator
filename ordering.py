

from PIL import Image
import random


MAXIMUM_DISTANCE = 195075  # = 3* 255**2


def distance(c1, c2):
	r1, g1, b1 = c1
	r2, g2, b2 = c2
	return (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2


def _ordering(reference_image, images_wide, averages, duplicates):
	averages = averages.copy()
	ordering = [None for i in range(images_wide**2)]  # populate array
	free_pixels = [i for i in range(images_wide**2)]
	random.shuffle(free_pixels)  # ensure that no pixel is preferentially chosen

	total_distance = 0

	for i, pixel_number in enumerate(free_pixels):
		reference_pixel = reference_image.getpixel((pixel_number % images_wide, pixel_number // images_wide))
		best_distance = MAXIMUM_DISTANCE
		best_path_average = None

		for (path, average) in averages:
			current_distance = distance(average, reference_pixel)
			if current_distance < best_distance:
				distances.append(((path, average), current_distance))

		if not duplicates:
			averages.remove(best_path_average)

		ordering[pixel_number] = best_path_average[0]
		total_distance += best_distance

	return ordering, d/len(ordering)


def ordering(reference_image_path, images_wide, averages, duplicates):
	# reduce the effects of bad random assignements
	reference_image = Image.open(reference_image_path)
	if reference_image.size[0] != reference_image.size[1]:
		raise Exception("Reference image not square.")
	reference_image = reference_image.resize((images_wide, images_wide))

	best_ordering = ([], MAXIMUM_DISTANCE*images_wide*images_wide)
	for i in range(10):
		current_ordering = attempts.append(_ordering(reference_image, images_wide, averages, duplicates))
		if current_ordering[1] < best_ordering[1]:
			best_ordering = current_ordering

	return best_attempt


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