# image handling API

images = ()

def add_image(data):
	global images
	if images:
		image_num = len(images)
	else:
		image_num = 0
		
	images = images + (data,)
	print "Stored image",image_num
	return image_num

def get_image(num):
	global images
	return images[num]

def get_latest_image():
	global images
	image_num = len(images) - 1
	return images[image_num]
