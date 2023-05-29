# An Instagram video/image downloader

# Watch Video Tutorial [HERE](https://youtu.be/4FzYyARA_ak)

## UPDATE

Due to Instagram restrictions, one must be logged in to be able to view videos and images, which is why you need to specify `-u` and `-p` flags

Due to Instagram hashing, masking and cloaking algorithm, getting the download link of a video is extremely tedius, which is why I had to get all XHR request (using selenium-wire) and reverse engineer those requests which we can use to download the audio and video separately, and combined these using ffpmeg

## REQUIREMENTS

All requirements for python are in the `requirements.txt` file

### FFMPEG INSTALLATION

<details>
<summary>How To Install FFMPEG</summary>

Confirm that you have installed ffmpeg by running `ffmpeg` and it isn't installed, do this

#### Windows:

1. Visit the official FFmpeg website at https://ffmpeg.org/download.html.
2. Scroll down to the "Windows" section and click on the link corresponding to "Windows Builds" to access the download page.
3. On the download page, you will find multiple options. Choose the one that matches your system architecture (32-bit or 64-bit).
4. Download the static build of FFmpeg by clicking on the "Download Build" link.
5. Extract the downloaded ZIP file to a location on your computer.
6. Add the FFmpeg binary path to your system's PATH environment variable. This step allows you to run FFmpeg from the command line without specifying the full path. Here's how you can add it:

   - Open the Start menu and search for "Environment Variables."
   - Click on "Edit the system environment variables."
   - In the System Properties window, click on the "Environment Variables" button.
   - In the "System variables" section, scroll down and select the "Path" variable.
   - Click on the "Edit" button.
   - Click on the "New" button and add the path to the folder where you extracted the FFmpeg binaries (e.g., C:\ffmpeg\bin).
   - Click "OK" to save the changes.

7. Open a new command prompt window and type ffmpeg to verify that FFmpeg is correctly installed. You should see the FFmpeg command-line tool information printed in the console.

#### macOS:

1. The easiest way to install FFmpeg on macOS is by using Homebrew. Open the Terminal application.
2. If you don't have Homebrew installed, run the following command to install it:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. Once Homebrew is installed, you can install FFmpeg by running the following command:

   ```bash
   brew install ffmpeg
   ```

4. Wait for the installation to complete. Homebrew will download and install the FFmpeg package along with its dependencies.
5. After the installation finishes, you can verify that FFmpeg is installed by typing ffmpeg in the Terminal. The FFmpeg command-line tool information should be displayed.

#### Linux (Ubuntu/Debian):

1. Open a terminal window.
2. Run the following command to install FFmpeg:

   ```bash
   sudo apt-get update
   sudo apt-get install ffmpeg
   ```

3. Wait for the installation to complete. The package manager will download and install FFmpeg along with its dependencies.
4. After the installation finishes, you can verify that FFmpeg is installed by typing ffmpeg in the terminal. The FFmpeg command-line tool information should be displayed.
</details>

### All Arguments

`-v` or `--video` = Specify the link is a video link e.g `python main.py -v`

`-i` or `--image` = Specify the link is an image link e.g `python main.py -i`

`-l` or `--link` = Link to image/video e.g `python main.py -i -l https://www.instagram.com/p/CEYfEKHDTo6/`

`-u` or `--username` = Add account username e.g `python main.py -i -u username https://www.instagram.com/p/CEYfEKHDTo6/`

`-p` or `--password` = Add account password e.g `python main.py -i -u username -p password https://www.instagram.com/p/CEYfEKHDTo6/`

`-f` or `--filename` = Name of the file with extention e.g `python main.py -i -l https://www.instagram.com/p/CEYfEKHDTo6/ -f downloaded.jpg`

## How to use

1. MAKE SURE you have ffmpeg installed, [read this manual above](#ffmpeg-installation)

2. Download chromedriver from https://chromedriver.chromium.org/downloads

3. Copy the `chromediver.exe` to `./chromedriver` path

4. Install the requirements by running `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`

5. Check argument variables and

6. Run `python main.py [options] -u username -p password -f filename.[ext]`
