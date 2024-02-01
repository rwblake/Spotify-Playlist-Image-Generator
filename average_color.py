

def get_dominant_colors(image_paths):
	from imagedominantcolor import DominantColor
	return [(path, DominantColor(path).rgb) for path in image_paths]


def get_mean_colors(image_paths):
	import cv2
	import numpy
	ret = []
	for path in image_paths:
		ret.append((path, list(numpy.average(numpy.average(cv2.imread(path), axis=0), axis=0))[::-1]))
	return ret


def get_average_colors(image_paths):
	# averages = [(path, average)]
	return get_mean_colors(image_paths)


def main():
	import os
	image_paths = os.listdir(".")
	print(get_average_colors(image_paths))


if __name__ == "__main__":
	main()