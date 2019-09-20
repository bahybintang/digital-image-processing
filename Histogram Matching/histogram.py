import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def generate_histogram(img):
    histogram = np.zeros(256)
    for pixel in img:
        histogram[pixel] += 1
    return histogram
    
def generate_cumprob (img):
    size = len(img)
    histogram = generate_histogram(img)
    cumprob = np.zeros(256)
    for i in range(256):
        if i == 0:
            cumprob[i] = histogram[i] / size
        else:
            cumprob[i] = cumprob[i-1] + histogram[i] / size
    return cumprob

def match (img1, img2):
    imga1 = np.asarray(img1)
    flat1 = imga1.flatten()
    imga2 = np.asarray(img2)
    flat2 = imga2.flatten()
    cumprob1 = generate_cumprob(flat1)
    cumprob2 = generate_cumprob(flat2)
    pixel_map = np.zeros(256)
    for i in range(256):
        for j in range(255):
            if cumprob1[i] >= cumprob2[j] and cumprob1[i] <= cumprob2[j+1]:
                if(cumprob1[i] - cumprob2[j] > cumprob2[j+1] - cumprob1[i]):
                    pixel_map[i] = j+1
                else:
                    pixel_map[i] = j
    pixel_map[255] = 255
    pixels = img1.load()
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            img1.putpixel((i, j), (int(pixel_map[pixels[i, j][0]]), int(pixels[i, j][1])))
    # img1.show()
    return img1

if __name__ == '__main__':
    img1 = Image.open("image1.jpg").convert('LA')
    img2 = Image.open("image2.jpg").convert('LA')
    img3 = Image.open("image3.jpg").convert('LA')
    match(img1, img2).convert("RGB").save("image1_2.jpg")
    match(img1, img3).convert("RGB").save("image1_3.jpg")
    match(img2, img1).convert("RGB").save("image2_1.jpg")
    match(img2, img3).convert("RGB").save("image2_3.jpg")
    match(img3, img1).convert("RGB").save("image3_1.jpg")
    match(img3, img2).convert("RGB").save("image3_2.jpg")