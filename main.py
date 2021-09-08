from bImage import bImage
import PIL.Image as Image
from bImage import bImage
import random
import os
# 合并图片的款高
iWidth = 800
iHeight = 600
savePath = r"C:\Users\lsk\Desktop\bimages"
# 分组标识
indexx = 0
# 图片间隙
clearance = 5



def getImageList(sourcePath):
    imageList = []
    fileList = os.listdir(sourcePath)
    for file in fileList:
        if(file.lower().endswith(('.bmp',  '.png', '.jpg', '.jpeg'))):
            imgPath = sourcePath+"//"+file
            from_image = Image.open(imgPath)
            img = {}
            img["path"] = imgPath
            img["width"] = from_image.size[0]
            img["height"] = from_image.size[1]
            img["intName"] = img['width']*img['height']
            imageList.append(img)
    return imageList

#二叉树横向排列图片并分组
def beeTreeWidth(imageList, bImageList, x, y, indexx, hhh, www):
    for idata in imageList:
        width = idata['width']+clearance
        height = idata['height']+clearance
        x1 = x + width
        y1 = y + height
        if x1 <= www and y1 <= hhh:
            bimg = bImage(idata['path'], x, y, indexx)
            bImageList.append(bimg)
            imageList.remove(idata)
            x2 = x
            y2 = y1
            bImageList = beeTreeWidth(imageList, bImageList,
                                 x2, y2, indexx, hhh, www)
            x3 = x1
            y3 = y
            bImageList = beeTreeWidth(imageList, bImageList,
                                 x3, y3, indexx, y1, www)
            break
    return bImageList


def takeSecond(elem):
    return elem['intName']


def hebingImage(issort=1, imageList1=[], savePath=savePath):
    # 根据图片面积排序
    if issort == 1:
        imageList1.sort(key=takeSecond, reverse=True)
    if issort == 0:
        imageList1.sort(key=takeSecond, reverse=False)
    bImageList = []
    global indexx
    while len(imageList1) > 0:
        bImageList = beeTreeWidth(imageList1, bImageList, 0,
                             0, indexx, iHeight, iWidth)
        indexx += 1
    bImageListList = {}
    for bimg in bImageList:
        bImageList1 = []
        if bimg.index in bImageListList.keys():
            bImageList1 = bImageListList[bimg.index]
        bImageList1.append(bimg)
        bImageListList[bimg.index] = bImageList1
    print(len(bImageListList))

    for index in bImageListList.keys():
        bImageList2 = bImageListList[index]
        to_image = Image.new('RGBA', (iWidth, iHeight))
        #  ,random_color())  # 创建一个新图
        for bimg in bImageList2:
            from_image = Image.open(bimg.path).convert("RGBA")
            width = from_image.size[0]
            height = from_image.size[1]
            from_image1 = Image.new(
                'RGBA', (width, height), random_color())  # 创建一个新图
            from_image1.alpha_composite(from_image, (0, 0))
            from_image = from_image1
            to_image.alpha_composite(from_image, (bimg.x, bimg.y))
        to_image.save(savePath+r"\000" +
                      str(index)+".png")  # 保存新图
    bImageListList.clear()

# 随机颜色值


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


if __name__ == '__main__':
    imageList1 = getImageList(r"./testImage")
    hebingImage(issort=1, imageList1=imageList1,
                savePath=r"./newImage")
