import os
import cv2
import numpy as np
import json
from urllib.request import urlopen


def download_images(json_fp):
    with open(json_fp, "r") as fp:
        data = json.load(fp)
    for rec in data:
        sku = rec['SKU']
        recsplit = rec['Category'].split('>')
        category = recsplit[1].strip()
        print(category)
        try:
            resp = urlopen(rec['Image'])
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        except:
            pass
        try:
            os.stat("images/" + category )
        except:
            os.mkdir("images/" + category)
        cv2.imwrite("images/" + category + "/" + str(sku) + ".jpg", image)
        print("done")


data = download_images("/home/jugs/PycharmProjects/ExperimentalProjects/new_chic/DataFeedNC.json")
