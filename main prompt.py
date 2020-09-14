from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import shutil
import time
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--video", help="Specify the link is a video link",
#                     action="store_true")
# parser.add_argument("-i", "--image", help="Specify the link is an image link",
#                     action="store_true")
# parser.add_argument("-l", "--link", type=str,
#                     help="Link to image/video")
# parser.add_argument("-f", "--filename", type=str,
#                     help="Name of the file with extention")
# args = parser.parse_args()

# Change this value to point to you downloaded chromedriver
CHROME_DRIVER_PATH = r'C:\Program Files\chromedriver\chromedriver.exe'

# AUTH IG USERNAME
username = ""

# AUTH IG PASSWORD
password = ""

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, options=options)


def downloadImage(url, filename):
    driver.get(url)
    s = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "FFVAD"))
    )
    s = s.get_attribute('src')
    r = requests.get(s, stream=True)

    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        print("Image Saved as " + filename)


def downloadVideo(url, filename):
    driver.get(url)
    s = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tWeCl"))
    )
    s = s.get_attribute('src')
    r = requests.get(s, stream=True)

    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
        print("Image Saved as " + filename)


def login():
    user_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    pswd_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    user_elem.send_keys(username)
    pswd_elem.send_keys(password+'\n')
    while 'Login' in driver.title:
        time.sleep(5)


# You can wrap this in a while loop to continously prompt the user.
# video, image, filename, link = args.video, args.image, args.filename, args.link
link = input("Input link to Instagram POST :: ")
image_or_video = input(
    "Input v if the link points to a video and i if it's an image :: ")
filename = input("Write a name you wish to save the file as :: ")

driver.get(link)
if 'Login' in driver.title:
    login()

if image_or_video == 'v':
    if filename.endswith('mp4') == False:
        filename = filename.split('.')[0]+'.mp4'
    downloadVideo(link, filename)
elif image_or_video == 'i':
    if filename.endswith('jpg') == False:
        filename = filename.split('.')[0]+'.jpg'
    downloadImage(link, filename)
else:
    print("WRONG INPUT")
driver.close()
