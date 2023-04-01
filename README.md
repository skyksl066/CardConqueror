# CardConqueror
CardConqueror is an automated card game program for Ragnarok Online Origin.

### Demo
![Image](https://github.com/skyksl066/CardConqueror/raw/main/img/sample.gif?raw=true)

## Environment
The program requires the following environment:
- [Python 3.9.13](https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe)
- Windows 10 x64
- [Ragnarok Online Origin]()

## Usage
### Clone the repository:
```bash
git clone git@github.com:skyksl066/CardConqueror.git
cd CardConqueror
```
### Install the necessary modules:
```bash
pip install -r requirements.txt
```
The requirements.txt file includes the following modules:
- opencv-python
- pyautogui
- pillow
- pywin32
- win32gui
- keyboard

### Open the game and enter the card game mode.
### Run the script:
```bash
python app.py
```

Before running the script, make sure to open the game and enter the card game mode. You should see the words "Start Challenge" on the screen.

If you want to interrupt the program, please press F12.

## Troubleshooting
- If the program cannot locate the card coordinates, use the LocateCards(0.95, r'img/card.bmp') function to obtain the card coordinates and replace the coordinates in coords.
- To troubleshoot image recognition issues caused by environmental discrepancies, try using the LocateCards function to reposition the cards and update the coords variable with the new coordinates. Replace the images in the img folder if accurate coordinates cannot be obtained, and manually input the missing coordinates if all else fails. Note that the program will automatically disconnect and start a new game in an infinite loop after flipping all the cards. These steps can improve the performance of the Card Conqueror application by resolving issues with card position recognition.
- If the program cannot click on the "Start" or "Exit" button, replace the corresponding image file in the img folder.
- If you encounter the error "pygetwindow.PyGetWindowException: Error code from Windows: 5 - Access is denied", right-click and run the program as administrator.
- For any other issues, please leave a message in the Issues section, and I will try my best to respond as soon as possible.

## License
This project is licensed under the Apache-2.0 License - see the [LICENSE](https://github.com/skyksl066/CardConqueror/blob/main/LICENSE) file for details.
