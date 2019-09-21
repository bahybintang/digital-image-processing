import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def generate_histogram(img):
    histogram = np.zeros(256)
    for pixel in img:
        # print(pixel)
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
    imNew = Image.new(img1.mode, img1.size)
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            imNew.putpixel((i, j), int(pixel_map[pixels[i, j]]))
    return imNew

if __name__ == '__main__':
    img = []
    histogram = []
    for i in range(1, 4):
        img.append(Image.open('image' + str(i) + '.jpg').convert('L'))
        histogram.append(generate_histogram(np.asarray(img[i-1]).flatten()))
    
    matched = [ [], [], [] ]
    for i in range(3):
        for j in range(3):
            matched[i].append(match(img[i], img[j]))
    
    for i in range(3):
        for j in range(3):
            fig, ax = plt.subplots(nrows=3, ncols=2)
            if i != j:
                fig.suptitle("Matching Image " + str(i+1) + " dengan Image " + str(j+1))
                ax[0, 0].set_title("Histogram")
                ax[0, 1].set_title("Image")
                ax[0, 0].set_ylabel("Image Before")
                ax[1, 0].set_ylabel("Image to Match")
                ax[2, 0].set_ylabel("Image After")
                ax[0, 0].bar(np.arange(256), histogram[i])
                ax[1, 0].bar(np.arange(256), histogram[j])
                ax[0, 1].imshow(img[i])
                ax[1, 1].imshow(img[j])
                ax[2, 0].bar(np.arange(256), generate_histogram(np.asarray(matched[i][j]).flatten()))
                ax[2, 1].imshow(matched[i][j])
                plt.savefig("comp" + str(i+1) + "_" + str(j+1) + ".jpg")
                plt.clf()