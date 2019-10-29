import cv2
directory = "static/"

from PIL import Image
import numpy

def embose_img(imgPath):
    # defining azimuth, elevation, and depth
    ele = numpy.pi/2.2 # radians
    azi = numpy.pi/4.  # radians
    dep = 10.          # (0-100)

    # get a B&W version of the image
    img = Image.open(imgPath).convert('L') 
    # get an array
    a = numpy.asarray(img).astype('float')
    # find the gradient
    grad = numpy.gradient(a)
    # (it is two arrays: grad_x and grad_y)
    grad_x, grad_y = grad
    # getting the unit incident ray
    gd = numpy.cos(ele) # length of projection of ray on ground plane
    dx = gd*numpy.cos(azi)
    dy = gd*numpy.sin(azi)
    dz = numpy.sin(ele)
    # adjusting the gradient by the "depth" factor
    # (I think this is how GIMP defines it)
    grad_x = grad_x*dep/100.
    grad_y = grad_y*dep/100.
    # finding the unit normal vectors for the image
    leng = numpy.sqrt(grad_x**2 + grad_y**2 + 1.)
    uni_x = grad_x/leng
    uni_y = grad_y/leng
    uni_z = 1./leng
    # take the dot product
    a2 = 255*(dx*uni_x + dy*uni_y + dz*uni_z)
    # avoid overflow
    a2 = a2.clip(0,255)
    # you must convert back to uint8 /before/ converting to an image
    img2 = Image.fromarray(a2.astype('uint8'))
    imgName = imgPath.split("/")[-1] 
    img2.save(directory + imgName)

def applyFilters(IMG_PATH):
    img = cv2.imread(IMG_PATH)

    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

    edges = cv2.Canny(img, 100, 200)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    embose_img(IMG_PATH)
    imgName = IMG_PATH.split("/")[-1]
    
    cv2.imwrite(directory + "sobelx_" + imgName, sobelx)
    cv2.imwrite(directory + "sobely_" + imgName, sobely)
    cv2.imwrite(directory + "edges_" + imgName, edges)
    cv2.imwrite(directory + "gray_" + imgName, gray)
    cv2.imwrite(directory + "binary_" + imgName, im_bw)
    cv2.imwrite(directory + "hsv_" + imgName, img_hsv)

    return ["sobelx_" + imgName, "sobely_" + imgName, "edges_" + imgName,
                "gray_" + imgName, "binary_" + imgName, "hsv_" + imgName, "embose_" + imgName]
