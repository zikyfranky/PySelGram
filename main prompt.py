from selenium import webdriver
import requests
import shutil
import argparse

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

# Change this value to point to you downloaded chromedriver
CHROME_DRIVER_PATH = r'C:\Program Files\chromedriver\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, options=options)


def downloadImage(url, filename):
    driver.get(url)
    s = driver.find_element_by_class_name('FFVAD').get_attribute('src')
    r = requests.get(s, stream=True)

    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def downloadVideo(url, filename):
    driver.get(url)
    s = driver.find_element_by_class_name('tWeCl').get_attribute('src')
    print(s)
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
