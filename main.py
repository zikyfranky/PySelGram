from ntpath import join
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import shutil
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video", help="Specify the link is a video link",
                    action="store_true")
parser.add_argument("-i", "--image", help="Specify the link is an image link",
                    action="store_true")
parser.add_argument("-l", "--link", type=str,
                    help="Link to image/video")
parser.add_argument("-f", "--filename", type=str,
                    help="Name of the file with extention")
args = parser.parse_args()

dir_name = os.path.dirname(os.path.realpath(__file__))
c_driver = os.path.join(dir_name, 'chromedriver\chromedriver')


# Change this value to point to your downloaded chromedriver
CHROME_DRIVER_PATH = c_driver

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, options=options)

By.CLASS_NAME
def downloadImage(url, filename):
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "FFVAD"))
    )
    s = element.get_attribute('src')
    r = requests.get(s, stream=True)

    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def downloadVideo(url, filename):
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tWeCl"))
    )
    s = element.get_attribute('src')
    r = requests.get(s, stream=True)

    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)


video, image, filename, link = args.video, args.image, args.filename, args.link

if video:
    downloadVideo(link, filename)
elif image:
    downloadImage(link, filename)
driver.close()
