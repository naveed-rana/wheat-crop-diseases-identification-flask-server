import cv2
directory = "static/"


def applyFilters(IMG_PATH):
    img = cv2.imread(IMG_PATH)

    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

    edges = cv2.Canny(img, 100, 200)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    imgName = IMG_PATH.split("/")[-1]
    
    cv2.imwrite(directory + "sobelx_" + imgName, sobelx)
    cv2.imwrite(directory + "sobely_" + imgName, sobely)
    cv2.imwrite(directory + "edges_" + imgName, edges)
    cv2.imwrite(directory + "gray_" + imgName, gray)
    cv2.imwrite(directory + "binary_" + imgName, im_bw)

    return ["sobelx_" + imgName, "sobely_" + imgName, "edges_" + imgName,
                "gray_" + imgName, "binary_" + imgName]
