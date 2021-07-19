from PIL import Image


def resizer(image,requiredSize):
    width, height = image.size
    if height >= requiredSize or width >= requiredSize:
        tempHeight = height
        tempWidth = width

        while (tempHeight > requiredSize  or tempWidth > requiredSize):
            tempHeight = tempHeight / 1.1
            tempWidth = tempWidth / 1.1
        resizedImage = image.resize((int(tempWidth), int(tempHeight)), Image.ANTIALIAS)
    else:
        resizedImage = image
    return resizedImage

def crop(image):
    width, height = image.size
    centerY = height/2
    centerX = width/2
    if(width>height):
        croppedimage = image.crop((centerX-centerY, 0, centerX+centerY, height))
        return croppedimage

    if(height>width):
        croppedimage = image.crop((0, centerY-centerX, width, centerY+centerX))
        return croppedimage

    else:
        croppedimage = image
        return croppedimage