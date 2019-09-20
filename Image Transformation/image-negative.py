from PIL import Image


def negative(im):
    pixels = im.load()

    newImg = Image.open("Nezuko.png")

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if newImg.mode == "L":
                newImg.putpixel((i, j), 255 - pixels[i, j])
            else:
                newImg.putpixel(
                    (i, j), (255 - pixels[i, j][0], 255 - pixels[i, j][1], 255 - pixels[i, j][2]))

    newImg.save("negative.png")


def powerLawTransformation(imdef, filename):
    # Convert to image mode L : grayscale
    im = imdef.convert("L")
    newImg = Image.open("Nezuko.png").convert("L")

    # Load the pixel
    pixels = im.load()

    gamma = float(input())
    min = 999
    max = -1

    # Get the maximum and minimum value to perform normalization
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            G = (pixels[i, j])**gamma
            if G < min:
                min = G
            if G > max:
                max = G

    # Gamma correction and normalize
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            G = (pixels[i, j])**gamma
            G = (G-min)/(max-min)
            G = G * 254
            newImg.putpixel((i, j), int(G))

    newImg.save(filename)


if __name__ == '__main__':
    im = Image.open("Nezuko.png")
    negative(im)
    powerLawTransformation(im, "gamma1.png")
    powerLawTransformation(im, "gamma2.png")
