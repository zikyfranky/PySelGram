import argparse
import os
import re
import shutil
import subprocess
from glob import glob
from time import sleep, time

import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video", help="Specify the link is a video link",
                    action="store_true")
parser.add_argument("-i", "--image", help="Specify the link is an image link",
                    action="store_true")
parser.add_argument("-l", "--link", type=str,
                    help="Link to image/video")
parser.add_argument("-f", "--filename", type=str,
                    help="Name of the file with extention")
parser.add_argument("-u", "--username", type=str,
                    help="Username to log in as")
parser.add_argument("-p", "--password", type=str,
                    help="Password of the user to log in as")
args = parser.parse_args()


dir_name = os.path.dirname(os.path.realpath(__file__))
c_driver = os.path.join(dir_name, 'chromedriver', 'chromedriver')
c_service = Service(executable_path=c_driver)

# Change this value to point to your downloaded chromedriver
CHROME_DRIVER_PATH = c_driver
OUTPUT_EXT = ".done.mp4"

# Make sure ffmpeg is installed
try:
    subprocess.check_output(f"which ffmpeg", shell=True)
except subprocess.CalledProcessError:
    raise Exception("FFMPEG is not installed!")

options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")

driver = webdriver.Chrome(service=c_service, options=options)


def login(username, password):
    driver.get("https://instagram.com")
    user_data_name = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    user_data_password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    user_data_name.clear()
    user_data_password.clear()
    user_data_name.send_keys(username)
    user_data_password.send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()
    sleep(10)  # Sleep for 10 seconds


def downloadImage(url, filename):
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[contains(@id, "mount_0_0_")]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div[1]/div/div/div/div/div/div/div[1]/img'))
    )
    s = element.get_attribute('src')
    r = requests.get(s, stream=True)

    print(s, filename)
    if (filename == None):
        filename = f"{time()}.png"
    print(s, filename)

    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def downloadVideo(url, filename):
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )
    s = element.get_attribute('src')
    if (filename == None):
        filename = f"{time()}"

    driver.wait_for_request("^.*\.mp4.*bytestart.*$", 20)

    includedFiles = []
    mediaFiles = []

    for request in driver.requests:
        if request.response and request.response.status_code == 200 and re.search("^.*\.mp4.*bytestart.*$", request.url) != None:
            key = re.search("\d/\d*.*\.mp4", request.url)
            if key:
                if (key.group(0) not in includedFiles):
                    mediaFiles.append(request.url.split("bytestart")[0])
                    includedFiles.append(key.group(0))

    r = requests.get(mediaFiles[0], stream=True)
    with open(filename+".mp4", 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)

    for index in [-1, -2]:
        r = requests.get(mediaFiles[index], stream=True)
        with open(f"{filename}{index}.mp3", 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

    combineAudioWithVideo(filename)


def cleanUp(filename):
    directory = os.path.dirname(os.path.realpath(__file__))
    pattern = os.path.join(directory, filename)
    file_paths = glob(f"{pattern}*")
    print("Deleting redundant files...")
    for file_path in file_paths:
        if (not file_path.endswith(OUTPUT_EXT)):
            os.remove(file_path)


def getAudioAndVideoFiles(filename):
    initialVideo = f"{filename}.mp4"
    firstAudio = f"{filename}-1.mp3"
    secondAudio = f"{filename}-2.mp3"

    size1 = os.path.getsize(firstAudio)
    size2 = os.path.getsize(secondAudio)
    size3 = os.path.getsize(initialVideo)

    potentialHDVideoFile = ""
    audioFile = ""
    videoFile = ""

    if size1 < size2:
        audioFile = firstAudio
        potentialHDVideoFile = secondAudio
    elif size1 > size2:
        audioFile = secondAudio
        potentialHDVideoFile = firstAudio
    else:
        audioFile = firstAudio
        potentialHDVideoFile = secondAudio

    hdSize = os.path.getsize(potentialHDVideoFile)

    if hdSize < size3:
        videoFile = initialVideo
    elif hdSize > size2:
        videoFile = potentialHDVideoFile
    else:
        videoFile = initialVideo

    return (videoFile, audioFile)


def combineAudioWithVideo(filename):
    video, audio = getAudioAndVideoFiles(filename)

    print("Audio file ", audio)
    print("Video file ", video)

    fullFile = f"{filename}{OUTPUT_EXT}"

    subprocess.run(['ffmpeg', '-i', video, '-i', audio,
                   '-c', 'copy', f"{fullFile}"])
    cleanUp(filename)

    for i in range(4):
        print()

    print("Video download complete")
    print("Video saved to", fullFile)


video, image, filename, link, username, password = args.video, args.image, args.filename, args.link, args.username, args.password

login(username, password)


if video:
    downloadVideo(link, filename)
elif image:
    downloadImage(link, filename)
driver.close()
