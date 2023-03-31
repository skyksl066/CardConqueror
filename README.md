# CardConqueror
CardConqueror is an automated card game program for Ragnarok Online Origin.

### Demo
![Image](https://github.com/skyksl066/CardConqueror/raw/main/img/sample.gif?raw=true)

## Environment
The program requires the following environment:
- Python 3.9.13
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

If you want to interrupt the program, please press F12.

## Troubleshooting
- If the program cannot locate the card coordinates, use the LocateCards(0.95, r'img/card.bmp') function in the program to obtain the card coordinates, and replace the coordinates in coords.
- If the program cannot click on the "Start" or "Exit" button, replace the corresponding image file in the img folder.
- If you encounter the error "pygetwindow.PyGetWindowException: Error code from Windows: 5 - Access is denied", please right-click and run the program as administrator.

## License
This project is licensed under the Apache-2.0 License - see the [LICENSE](https://github.com/skyksl066/CardConqueror/blob/main/LICENSE) file for details.
