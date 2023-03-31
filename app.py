# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 08:35:16 2023

@author: AlexKuo
"""
import cv2
import pyautogui
import numpy as np
from PIL import ImageGrab
import time
import threading
import random
import os
import win32gui
import keyboard


def init(hwnd):
    '''初始化'''
    print('Initialization')
    print('Current window position:', hwnd.left, hwnd.top)
    print('Current window size:', hwnd.width, hwnd.height)
    if hwnd.isActive is False:
        hwnd.activate()
        print('Activate')
    hwnd.moveTo(0, 0)
    print('MoveTo: 0, 0')
    hwnd.resizeTo(960, 540)
    print('ResizeTo: 960, 540')

def restore(hwnd, pos, size):
    print('Restore')
    print(f'MoveTo: {pos[0]}, {pos[1]}')
    hwnd.moveTo(pos[0], pos[1])
    print(f'ResizeTo: {size[0]}, {size[1]}')
    hwnd.resizeTo(size[0], size[1])


def PrintScreen(left, top, rignt, bottom, path):
    '''螢幕區域截圖'''
    # 截取整個螢幕
    screenshot = ImageGrab.grab()
    # 裁切區域（左、上、右、下）
    cropped_region = screenshot.crop((left, top, rignt, bottom))
    # 將裁切後的圖片存成檔案（bmp）
    # cropped_region.save(path)
    return np.array(cropped_region)


def LocateCards(threshold, template_path):
    '''定位圖像在螢幕上的座標'''
    screenshot = ImageGrab.grab()
    image = cv2.imread(template_path)
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, image_gray, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    # 返回所有卡片中心點的座標
    return list(zip(*locations[::-1]))


def mse(image1, image2):
    """比對圖片"""
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image2.shape[1])
    return err


def waitAndCapture(coord, i):
    '''等待卡片翻開並進行截圖'''
    global cards
    time.sleep(0.38)
    left, top = coord
    right = left + 50
    bottom = top + 50
    path = os.path.join(dir_path, rf'card\{i}.bmp')
    cards.append({'img': PrintScreen(left, top, right, bottom, path), 'index': i})


def matchCard():
    '''比對卡片'''
    global cards, match, start, used_idx
    # 進行匹配
    while start:
        for i in cards:
            if i['index'] in used_idx:
                continue
            for j in cards:
                if i['index'] == j['index'] or j['index'] in used_idx:
                    continue
                # 轉換成灰階圖像
                gray1 = cv2.cvtColor(i['img'], cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(j['img'], cv2.COLOR_BGR2GRAY)
                # 計算MSE值
                mse_value = mse(gray1, gray2)
                if mse_value < 1800:
                    if i['index'] % 2 == 0 and j['index'] % 2 == 1 and j['index'] - i['index'] == 1:
                        pass
                    else:
                        match.append([i['index'], j["index"]])
                    used_idx.add(i['index'])
                    used_idx.add(j["index"])
        time.sleep(0.01)


def clickCard(card_index, screen=False):
    '''點擊卡片'''
    global times
    pyautogui.click(coords[card_index][0]+20, coords[card_index][1]+20, _pause=False)
    time.sleep(CLICK_DELAY)
    times += 1
    if screen:
        pyautogui.moveTo(coords[card_index + 1][0]+10, coords[card_index + 1][1]+10, _pause=False)
        t = threading.Thread(target=waitAndCapture, args=(coords[card_index], card_index))
        t.start()


def removeCards(matched_cards):
    '''移除已存在的卡片'''
    global cards
    cards = [card for card in cards if card['index'] not in matched_cards]


def main():
    global times, cards, start, used_idx, match
    again = 0
    count = 0
    while again < 2:
        cards = []
        match = []
        start = True
        times = 0
        toolong = 0
        used_idx = set()
        count += 1
        print(f'Game: {count}')
        # 開始遊戲
        pos = LocateCards(0.95, os.path.join(dir_path, r'img\start.bmp'))
        if len(pos) > 0:
            print('StartGame')
            pyautogui.click(pos[0])
            time.sleep(START_DELAY)
        start_time = time.time()
        loop = threading.Thread(target=matchCard)
        loop.start()
        for i in range(20):
            clickCard(i, True)
        print("Time spent clicking the card: ", time.time() - start_time, "sec")
        match_time = time.time()
        while True:
            toolong += 1
            if len(used_idx) >= 8:
                #print(f'match: {len(match)} used_idx: {len(used_idx)}')
                print("Time spent recognizing: ", time.time() - match_time, "sec")
                match_time = time.time()
                for a, b in match:
                    clickCard(a)
                    clickCard(b)
                lack = set(range(20)) - used_idx
                lack = list(lack)
                # 逐一比較相鄰元素
                j = 0
                while j < len(lack) - 1:
                    if (lack[j] - lack[j+1] == -1) and (lack[j] % 2 == 0) and (lack[j+1] % 2 == 1) and (lack[j] not in[18, 19]):
                        # 如果符合條件，就將這兩個元素從列表中移除
                        lack.pop(j)
                        lack.pop(j)
                    else:
                        # 如果不符合條件，就繼續比較下一對相鄰元素
                        j += 1
                random.shuffle(lack)
                #print(f'lack: {lack}')
                for i in lack:
                    clickCard(i)
                break
            if toolong > 200:
                toolong = 0
                break
            time.sleep(0.01)
        print("Time spent clicking: ", time.time() - match_time, "sec")
        start = False
        #print(f'match: {match}')
        time.sleep(1)
        # 離開遊戲
        pos = LocateCards(0.95, os.path.join(dir_path, r'img\exit.bmp'))
        if len(pos) > 0:
            print('ExitGame')
            pyautogui.click(pos[0])
            time.sleep(0.5)
            pyautogui.click(548, 360)
            time.sleep(0.5)
        # 再來一局
        pos = LocateCards(0.95, os.path.join(dir_path, r'img\again.bmp'))
        if len(pos) > 0:
            again += 1
            print(f'Again: {again}')
            pyautogui.click(pos[0])
            time.sleep(START_DELAY)
            end_time = time.time()
            print("Total execution time: ", end_time - start_time -1.5, "sec")
            with open(os.path.join(dir_path, 'cards.txt'), 'a') as f:
                f.write(','.join(map(str, match))+'\n')
    

def startGame(hwnd):
    hwnd.restore()
    originalPos = [hwnd.left, hwnd.top]
    originalSize = [hwnd.width, hwnd.height]
    init(hwnd)
    time.sleep(1)
    main()
    restore(hwnd, originalPos, originalSize)


def monitor(key):
    '''強制停止程序'''
    if key.name == 'f12':
        print("F12 key pressed, exiting program")
        os._exit(1)


coords = [(192, 85), (192, 192), (192, 299), (192, 406), 
          (299, 85), (299, 192), (299, 299), (299, 406),
          (405, 85), (405, 192), (405, 299), (405, 406),
          (512, 85), (512, 192), (512, 299), (512, 406), 
          (619, 85), (619, 192), (619, 299), (619, 406), (192, 85)]
used_idx = set()
match = []
CLICK_DELAY = 0.33
START_DELAY = 0.42
# 取得主程式所在的目錄路徑
dir_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    keyboard.on_press(monitor)
    hwnd = pyautogui.getWindowsWithTitle("RO仙境傳說：愛如初見")
    if len(hwnd) == 0:
        print("I don't found windows.")
    if len(hwnd) >= 1:
        Input = input(f'I found {len(hwnd)} windows. Which one should I execute? {list(range(len(hwnd)))} or ALL: ').upper()
        asw = 'N'
        while asw == 'N':
            asw = input('Please prepare the game first until you can see the "Start Challenge" button. Are you ready? [Y, N] default:[Y]: ').upper()
            if asw == '':
                asw = 'Y'
        if asw == 'Y':
            if Input.isdigit():
                num = int(Input)
                startGame(hwnd[num])
            elif 'ALL' in Input:
                length = len(hwnd)
                for i in range(length):
                    # 暫時修改標題
                    win32gui.SetWindowText(hwnd[i]._hWnd, f"ROO:{i}")
                    hwnd[i].minimize()
                for i in range(length):
                    # print(i)
                    h = pyautogui.getWindowsWithTitle(f"ROO:{i}")[0]
                    startGame(h)
                    time.sleep(0.2)
                    h.minimize()
                    win32gui.SetWindowText(h._hWnd, "RO仙境傳說：愛如初見")
                hwnd = pyautogui.getWindowsWithTitle("RO仙境傳說：愛如初見")
                for h in hwnd:
                    h.restore()
