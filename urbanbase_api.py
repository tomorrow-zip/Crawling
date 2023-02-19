import requests
import json
import io
import numpy as np
import cv2
import base64

import time

import pandas as pd
import os

from matplotlib import pyplot as plt
from tqdm import tqdm
from glob import glob

detector_url = "https://apis.openapi.sk.com/urbanbase/v1/space/detector"
analyzer_url = "https://apis.openapi.sk.com/urbanbase/v1/space/analyzer"

headers = {
    "accept": "application/json",
    "Content-Type": "json",
    "appKey": "{Your Key}"
}


def caller(url, payload, headers):
    return requests.post(url, data=payload, headers=headers)


def get_analysis_from_furniture_id(furniture_id: int):
    url = os.path.join('http://35.216.58.5:5000', 'static', 'img', 'furniture', f'{furniture_id}-0.jpg')
    payload = str(json.dumps({'image_path': url}))

    res = json.loads(caller(analyzer_url, payload, headers).text)

    print(res)
    time.sleep(0.5)

    if res["code"] != "00000":
        res['FurnitureId'] = furniture_id

    return res


if __name__ == "__main__":
    csvs = sorted(glob('*.csv'))

    for csv in csvs[1:]:
        furniture_sets = pd.read_csv(csv, names=['FurnitureId', 'URL', 'Images'])
        furniture_ids = pd.unique(furniture_sets['FurnitureId'])

        results = []

        for furniture_id in tqdm(furniture_ids):
            results.append(get_analysis_from_furniture_id(furniture_id))

        with open(f'analysis_result_{os.path.splitext(csv)[0]}.json', 'w+') as f:
            json.dump(results, f)
