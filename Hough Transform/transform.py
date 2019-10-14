import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math
import random

def convolve(imgM, kx, ky):
    maxs = [-1, -1, -1]
    img = imgM.load()
    tmp = [-1, 0, 1]

    imGaus = Image.new(imgM.mode, imgM.size)
    #  Gaussian
    for x in range(imgM.size[0]):
        for y in range(imgM.size[1]):
            sums = 0
            for i in range(3):
                for j in range(3):
                    posX = x + tmp[i]
                    posY = y + tmp[j]
                    if posX >= 0 and posX < imgM.size[0] and posY >= 0 and posY < imgM.size[1]:
                        sums += img[posX, posY] / 9
            if x == 0 or x == imgM.size[0] - 1 or y == 0 or y == imgM.size[1] - 1:
                if x == 0:
                    imGaus.putpixel((x, y), img[x + 1, y])
                elif y == 0:
                    imGaus.putpixel((x, y), img[x, y + 1])
                elif x == imgM.size[0] - 1:
                    imGaus.putpixel((x, y), img[imgM.size[0] - 2, y])
                elif y == imgM.size[1] - 1:
                    imGaus.putpixel((x, y), img[x, imgM.size[1] - 2])
            else:
                imGaus.putpixel((x, y), int(sums))
                
    img = imGaus.load()
    imNew = Image.new(imgM.mode, imgM.size)

    for x in range(imgM.size[0]):
        for y in range(imgM.size[1]):
            sumX = 0
            sumY = 0
            for i in range(3):
                for j in range(3):
                    posX = x + tmp[i]
                    posY = y + tmp[j]
                    if posX >= 0 and posX < imgM.size[0] and posY >= 0 and posY < imgM.size[1]:
                        sumX += img[posX, posY] * kx[i][j]
                        sumY += img[posX, posY] * ky[i][j]
            val = math.sqrt(sumX*sumX + sumY*sumY)
            if x == 0 or x == imgM.size[0] - 1 or y == 0 or y == imgM.size[1] - 1:
                imNew.putpixel((x, y), 0)
            else:
                imNew.putpixel((x, y), int(val))
            val = imNew.getpixel((x, y))
            if val > maxs[2] and val != maxs[1] and val != maxs[0]:
                if val > maxs[1]:
                    if val > maxs[0]:
                        maxs[2] = maxs[1]
                        maxs[1] = maxs[0]
                        maxs[0] = val
                    else:
                        maxs[2] = maxs[1]
                        maxs[1] = val
                else:
                    maxs[2] = val

    print (maxs[2])
    img = imNew.load()
    for x in range(imgM.size[0]):
        for y in range(imgM.size[1]):
            if (img[x, y] >= maxs[2]):
                imNew.putpixel((x, y), 255)
            else:
                imNew.putpixel((x, y), 0)

    return imNew

def sobel_filter(img):
    Kx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]

    Ky = [
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ]

    return convolve(img, Kx, Ky)

def hough_transform(imgM):
    maxs = int(math.sqrt(imgM.size[0] * imgM.size[0] + imgM.size[1] * imgM.size[1]))
    graf = []
    freq = [[0 for x in range(181)] for y in range(maxs * 2 + 1)] 
    # imNew = Image.new(mode="RGB", size=(181, maxs * 2 + 1))

    for i in range(181):
        graf.append([])

    for x in range(imgM.size[0]):
        for y in range(imgM.size[1]):
            if imgM.getpixel((x, y)) == 255:
                for i in range(181):
                    sudut = (i - 90) % 360
                    rho = int(x * math.cos(math.radians(sudut)) + (imgM.size[1] - y - 1) * math.sin(math.radians(sudut)))
                    # graf.append([sudut, rho])
                    graf[i].append(rho)
                    freq[maxs + rho][i] += 1
                    # rho = rho / maxs
                    # print(str(i) + " " + str(rho))
                    # imNew.putpixel((i, int(maxs + rho)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    hehe = []
    for i in range(maxs * 2 + 1):
        for j in range(181):
            hehe.append(( j - 90, i - maxs, freq[i][j] ))
    
    hehe = sorted(hehe, key = getKey, reverse = True)
    hehe = hehe[:3]
    return graf, hehe

def getKey(item):
    return item[2]

def garis(newIm, freq):
    for i in range(3):
        for x in range(newIm.size[0]):
            for y in range(newIm.size[1]):
                if freq[i][1] == int(x * math.cos(math.radians(freq[i][0])) + (newIm.size[1] - y - 1) * math.sin(math.radians(freq[i][0]))):
                    newIm.putpixel((x, y), (255, 0, 0))
    return newIm

if __name__ == '__main__':
    img = []
    sobel = []
    for i in range(4):
        img.append(Image.open('image' + str(i+1) + '.jpg').convert('L'))
        sobel.append(sobel_filter(img[i]))
        sobel[i].save('hasil' + str(i+1) + '.jpg')
        graf, freq = hough_transform(sobel[i])
        garis(Image.open('image' + str(i+1) + '.jpg').convert("RGB"), freq).save("garis" + str(i + 1) + ".jpg")
        # print (freq)
        # im.save("grafgambar" + str(i+1) + ".jpg")
        plt.plot(graf)
        plt.savefig("graf" + str(i+1) + ".jpg")
        plt.clf()

