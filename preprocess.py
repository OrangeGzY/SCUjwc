import cv2
import copy
from PIL import Image
import glob
import time
import matplotlib.pyplot as plt
import numpy

#file = '/Users/apple/Desktop/picturetrain/var1.jpg'

def openImage(file):
    img = cv2.imread(filename=file)
    #print(img[36][56])     #前y后x
    #i = image[36][56]
    #print(i[2])
    img_new = del_noise(img=img)
    img_bin=binary(img_new)
    image = Image.fromarray(cv2.cvtColor(img_bin, cv2.COLOR_BGR2RGB))
    Img = image.convert("L")
    table = get_bin_table()
    Img = Img.point(table,"1")
    region = (44, 10, 140, 57)
    croping = Img.crop(region) #图片切割后
    #croping2 = cv2.cvtColor(cv2.UMat(numpy.asarray(croping)), cv2.COLOR_BGR2GRAY)
    #del_noise2(croping)
    #croping.show()
    #Img.show()

    #image.show()
    #cv2.imshow("image",croping2)
    #cv2.waitKey(0)
    #return image
    return croping

def del_noise(img):
    count=0
    height = img.shape[0]
    width = img.shape[1]
    img_new = copy.deepcopy(img)
    for i in range(1,height-1):
        for j in range(1,width-1):
            up = img[i+1][j]
            down = img[i-1][j]
            tmp = img[i][j]
            if(tmp[0]==0 and tmp[1] == 0):
                count+=1
                img_new[i][j] = [0,0,255]
            elif(tmp[0]<=50 and tmp[1]<=50 and tmp[2]<=50):
                img_new[i][j] = [255, 255, 255]
    # print(count)
    # cv2.imshow("image", img_new)
    # cv2.waitKey(0)
    return img_new

def binary(img):
    height = img.shape[0]
    width = img.shape[1]
    for i in range(1,height-1):
        for j in range(1,width-1):
            if((img[i][j])[0] >=210):
                (img[i][j])=[255,255,255]

    # cv2.imshow("image" , img)
    # cv2.waitKey(0)
    return img

def get_bin_table(threshold=170):
    # 灰度转二值
    table=[]
    for i in range(256):
        if(i<threshold):
            table.append(0)
        else:
            table.append(1)
    return table

def del_noise2(data):
    w = data.width
    h = data.height
    count = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            #print(data.getpixel((x,y)),end = ',')
            if(data.getpixel((x,y+1))==1 and data.getpixel((x,y))==0 or
               data.getpixel((x,y-1))==1 and data.getpixel((x,y))==0 or
               data.getpixel((x, y - 1)) == 1 and data.getpixel((x, y+1)) == 1):
                # print("ok")
                data.putpixel((x,y),1)

    #data.show()

def cut(img,outDir,name,count=4,p_w=3,):
    w, h = img.size
    pixdata = img.load()
    eachWidth = int(w / count)
    beforeX = 0
    for i in range(count):

        allBCount = []
        nextXOri = (i + 1) * eachWidth

        for x in range(nextXOri - p_w, nextXOri + p_w):
            if x >= w:
                x = w - 1
            if x < 0:
                x = 0
            b_count = 0
            for y in range(h):
                if pixdata[x, y] == 0:
                    b_count += 1
            allBCount.append({'x_pos': x, 'count': b_count})
        sort = sorted(allBCount, key=lambda e: e.get('count'))

        nextX = sort[0]['x_pos']
        box = (beforeX, 0, nextX, h)
        img.crop(box).save(outDir+name[i]+'/'+ str(name)+'_'+str(i) + ".jpg")

        beforeX = nextX

if __name__ == '__main__':
    count=0
    filelist = []
    for file in glob.glob("/Users/apple/Desktop/after/*.jpg"):
        filelist.append(file)


    for i in range(1,996):
        file = filelist[i]
        file_name = file[-8:-4]
        image = openImage(file)
        cut(image,'/Users/apple/Desktop/cut/',file_name)
        count+=1
        print("第",count,'次切割')

    print("切割完成，一共",count,"张，请在 /Users/apple/Desktop/cut/ 下查看")




