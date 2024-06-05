

from PIL import Image
import random
from tqdm import tqdm



def distance(c1, c2):
	"Calculate Euclidian distance between two RGB(A) tuples, ignoring alpha"
	try:
		r1, g1, b1 = c1
		r2, g2, b2 = c2
	except ValueError:
		r1, g1, b1, _ = c1
		r2, g2, b2, _ = c2
	return (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2


def _ordering(reference_image, images_wide, averages, duplicates):
	averages = averages.copy()
	ordering = [None for i in range(images_wide**2)]  # populate array
	free_pixels = [i for i in range(images_wide**2)]
	random.shuffle(free_pixels)  # ensure that no pixel is preferentially chosen

	total_distance = 0
	uses = dict()

	for i, pixel_number in enumerate(free_pixels):
		reference_pixel = reference_image.getpixel((pixel_number % images_wide, pixel_number // images_wide))
		best_distance = float('inf')
		best_path_average = None

		for (path, average) in averages:
			current_distance = distance(average, reference_pixel)
			
			# avoid blocks of the same pixel by exponentially
			# increasing distance by number of previous assignments
			if duplicates:
				if path in uses:
					current_distance *= 1.03 ** uses[path]

			if current_distance < best_distance:
				best_distance = current_distance
				best_path_average = (path, average)

		if not duplicates:
			averages.remove(best_path_average)
		else:
			if best_path_average[0] in uses:
				uses[best_path_average[0]] += 1
			else:
				uses[best_path_average[0]] = 1

		ordering[pixel_number] = best_path_average[0]
		total_distance += best_distance

	return ordering, total_distance / len(ordering)


def ordering(reference_image_path, images_wide, averages, duplicates):
	# reduce the effects of bad random assignements
	reference_image = Image.open(reference_image_path)
	if reference_image.size[0] != reference_image.size[1]:
		raise Exception("Reference image not square.")
	reference_image = reference_image.resize((images_wide, images_wide))

	best_ordering = ([], float('inf'))
	for i in tqdm(range(10), total=10):
		current_ordering = _ordering(reference_image, images_wide, averages, duplicates)
		if current_ordering[1] < best_ordering[1]:
			best_ordering = current_ordering

	return best_ordering


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