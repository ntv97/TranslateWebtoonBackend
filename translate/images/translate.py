import cv2
import easyocr
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
from deep_translator import GoogleTranslator
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse

base = settings.MEDIA_ROOT + "/images/"
out = settings.MEDIA_ROOT + "/translated/"

def TranslateImage(filename):
    path = base + filename
    if not os.path.isfile(path):
        sys.exit(1)

    image = cv2.imread(path)

    LANGUAGE = "ko"
    reader = easyocr.Reader([LANGUAGE])
    result = reader.readtext(image)

    # Read the image
    img_rect = cv2.imread(path) #cv2.imread(image)
    img_temp = cv2.imread(path) #cv2.imread(image)
    h, w, c = img_temp.shape

    # Fill temp image with black
    img_temp = cv2.rectangle(img_temp, [0,0], [w, h], (0, 0, 0), -1)
    img_inpaint = cv2.imread(path) #cv2.imread(image)
    preview_rect = cv2.imread(path) #cv2.imread(image)

    raw_list = []
    rects = []
    for r in result:
        raw_list.append(r[1])
        bottom_left = tuple(int(x) for x in tuple(r[0][0]))
        top_right = tuple(int(x) for x in tuple(r[0][2]))
        rects.append((top_right, bottom_left))
        # Draw a rectangle around the text
        img_rect = cv2.rectangle(img_rect, bottom_left, top_right, (0,255,0), 3)
        # Fill text with white rectangle
        img_temp = cv2.rectangle(img_temp, bottom_left, top_right, (255, 255, 255), -1)
        # Convert temp image to black and white for mask
        mask = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(out + "mask.png", mask)
        # "Content-Fill" using mask (INPAINT_NS vs INPAINT_TELEA)
        img_inpaint = cv2.inpaint(img_inpaint, mask, 3, cv2.INPAINT_TELEA)
        cv2.imwrite(out + "inpaint.png", img_inpaint)
        # Draw a rectangle around the text
        preview_rect = cv2.rectangle(img_rect, bottom_left, top_right, (0,255,0), 3)
        # Draw confidence level on detected text
        cv2.putText(preview_rect, str(round(r[2], 2)), bottom_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, 1)
        cv2.imwrite(out + "rect.png", preview_rect)

    img = cv2.imread(out + "inpaint.png")
    threshold = 0.25
    for t_, t in enumerate(result):
        bbox, text, score = t
        translated = GoogleTranslator(source='ko', target='en').translate(text)

        if score > threshold:
            cv2.putText(img, translated, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), 2)
    img = cv2.resize(img, (640,640))
    cv2.imwrite(out + "translated.png", img)

    return out + "translated.png"


def ResizeImage(filename):
    path = base + filename
    if not os.path.isfile(path):
        sys.exit(1)

    img = cv2.imread(path)
    img = cv2.resize(img, (640,640))
    cv2.imwrite(base + "resized.png", img)

    return base + "resized.png"
