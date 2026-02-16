import pyautogui
import time
import cv2
import numpy as np
from PIL import ImageGrab
import os

# 设置
pyautogui.FAILSAFE = True
RED_PACKET_IMG = "red_packet.png"  # 红包图片
CLOSE_BTN_IMG = "close_btn.png"  # 关闭按钮


def find_image(template_path, confidence=0.8):
    """查找图片位置"""
    if not os.path.exists(template_path):
        return None

    # 截图
    screen = np.array(ImageGrab.grab())
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    # 模板匹配
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        h, w = template.shape[:2]
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)
    return None


def click(x, y):
    """点击"""
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()


def grab_red_packet():
    """抢红包"""
    # 找红包
    pos = find_image(RED_PACKET_IMG)
    if pos:
        print("发现红包！")
        click(pos[0], pos[1])  # 点击红包
        time.sleep(1)

        # 关闭
        close_pos = find_image(CLOSE_BTN_IMG)
        if close_pos:
            click(close_pos[0], close_pos[1])
        else:
            pyautogui.press('esc')
        print("抢完了")
        return True
    return False


def main():
    print("开始监控红包...")
    count = 0
    try:
        while True:
            pyautogui.scroll(-500)  # 向下滚动
            if grab_red_packet():
                count += 1
                print(f"已抢到 {count} 个")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n停止监控，共抢到 {count} 个红包")


if __name__ == "__main__":
    main()
