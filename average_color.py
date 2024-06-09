

def get_dominant_colors(image_paths):
	from imagedominantcolor import DominantColor
	return [(path, DominantColor(path).rgb) for path in image_paths]


def get_mean_colors(images):
	import numpy
	ret = []
	for image in images:
		average = numpy.average(image.getdata(), axis=0)
		if average.size == 3:
			# rgb
			ret.append((image, list(average)))
		else:
			# monochrome
			ret.append((image, (average, average, average)))
	return ret


def get_average_colors(images):
	"""averages = [(image, average), ...]"""
	return get_mean_colors(images)


def main():
	import os
	image_paths = os.listdir(".")
	print(get_average_colors(image_paths))


if __name__ == "__main__":
	main()