# Importing Necessary Libraries

import mss.tools
import cv2
import numpy as np
import urllib
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# List which stores the numerical representation of cards
cards = []

# Opening a Selenium Chrome instance
ser = Service(r"C:\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
driver.get("http://www.setgame.com/set/puzzle")

# Scraping the website for any image containing a Set card
imgResults = driver.find_elements(By.XPATH, "//img[contains(@class,'A')]")

# Storing all the cards as images
src = []
for img in imgResults:
    src.append(img.get_attribute('src'))

for i in range(12):
    urllib.request.urlretrieve(str(src[i]), "Card_{}.png".format(i))


def max_contour(img2):
    # Creating a grayscale image of the card, as well as blurring any insignificant markings
    gray1 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)

    # Limiting the image to only 2 possible pixel values, making little room for error when contouring
    ret1, edged1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edged1 = cv2.bitwise_not(edged1)

    # Finding the largest contour in the image
    contours1, hierarchy1 = cv2.findContours(edged1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    c1 = max(contours1, key=cv2.contourArea)

    return c1


# Compare two cards, and return a number corresponding to the similarity in shape
def compareCards(img1, img2):
    ret = cv2.matchShapes(max_contour(img1), max_contour(img2), 1, 0.0)
    return (ret)


# Find the number of shapes on the card
def findNumber(img2):
    # The number of shapes in the image
    count = 0

    # Creating a grayscale image of the card, as well as blurring any insignificant markings
    gray1 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)

    # Limiting the image to only 2 possible pixel values, making little room for error when contouring
    ret1, edged1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edged1 = cv2.bitwise_not(edged1)

    # Finding the largest contour in the image
    contours1, hierarchy1 = cv2.findContours(edged1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(contours1, key=cv2.contourArea, reverse=True)

    # Trying to find contours with a similar area to the largest contour
    areaTarget = cv2.contourArea(cnt[0])

    # If the area is similar to the largest contour, another shape has been found
    for i in range(len(cnt)):
        if (cv2.contourArea(cnt[i]) > areaTarget - 100 and cv2.contourArea(cnt[i]) < areaTarget + 100):
            count += 1

    return [count, cnt]


# Find the pattern of the card
def findPattern(count, cnt):
    # If the amount of shapes is equivalent to the amount of contours, the shape is solid
    if (count == len(cnt)):
        return 0  # SOLID

    # If the amount of shapes is equivalent to half the amount of contours, the shape is hollow
    elif (len(cnt) == count * 2):
        return 1  # HOLLOW

    # If the previous conditions aren't satisfied, the shape is shaded
    else:
        return 2  # SHADED


# Find the color of the card
def findColor(img1):
    # Set bounds for red color
    lowcolor = (0, 0, 233)
    highcolor = (128, 128, 255)

    # Count the amount of red pixels, if greater than 0, card is red
    thresh = cv2.inRange(img1, lowcolor, highcolor)
    count = np.sum(np.nonzero(thresh))

    if count > 0:
        return 0  # RED

    # If the count was 0, try again with bounds for the color green
    elif count == 0:
        lowcolor = (0, 150, 0)
        highcolor = (90, 255, 90)
        thresh = cv2.inRange(img1, lowcolor, highcolor)
        count = np.sum(np.nonzero(thresh))

        # Count the amount of green pixels, if greater than 0, card is green
        if count > 0:
            return 1  # GREEN

        # If the previous conditions aren't satisfied, the card is purple
        else:
            return 2  # PURPLE


# Find the shape of the card
def findShape(img1):
    # Check the similarity between the card, and an oval
    img2 = cv2.imread("OvalExample.jpg")
    if (compareCards(img1, img2) < .1):
        return 0  # OVAL

    # Check the similarity between the card, and a diamond
    img2 = cv2.imread("DiamondExample.png")
    if (compareCards(img1, img2) < .1):
        return 1  # DIAMOND

    # If the previous conditions aren't satisfied, the card is a squiggle
    else:
        return 2  # SQUIGGLE


# Calls all the previous attribute methods, and returns an array with their values
def findCardAttributes(img1):
    color = findColor(img1)
    numbers = findNumber(img1)
    number = (numbers[0])
    pattern = findPattern(numbers[0], numbers[1])
    shape = findShape(img1)
    return [color, number, pattern, shape]

# Append the images to the card array
for i in range(12):
    img2 = cv2.imread("Card_{}.png".format(i))
    cards.append(findCardAttributes(img2))

# Checks all of the possible card combinations.  If the attributes are divisible by 3, the attributes are either the same or different
for i in range(10):
    for j in range(i + 1, 11):
        for k in range(j + 1, 12):
            if (((cards[i][0] + cards[j][0] + cards[k][0]) % 3 == 0) and (
                    (cards[i][1] + cards[j][1] + cards[k][1]) % 3 == 0) and (
                    (cards[i][2] + cards[j][2] + cards[k][2]) % 3 == 0) and (
                    (cards[i][3] + cards[j][3] + cards[k][3]) % 3 == 0)):

                # Using selenium, the necessary cards are clicked
                card1 = driver.find_element(By.XPATH, "//img[@name='card{}']".format(i + 1))
                card1.click()

                card2 = driver.find_element(By.XPATH, "//img[@name='card{}']".format(j + 1))
                card2.click()

                card3 = driver.find_element(By.XPATH, "//img[@name='card{}']".format(k + 1))
                card3.click()

                # One second delay, allows the user to see what the script is doing.  Otherwise, the sets are achieved too quickly
                time.sleep(1)

