from PIL import Image

def convertImage(image):
	img = Image.open(image)
	img = img.convert("RGBA")

	datas = img.getdata()

	newData = []

	for items in datas:
		if items[0] == 0 and items[1] == 0 and items[2] == 0:
			newData.append((255, 255, 255, 0))
		else:
			newData.append(items)

	img.putdata(newData)
	img.save(image, "PNG")