import keyboard
import pyautogui
import cv2
import numpy as np
import os
from PIL import Image
import pyperclip
from io import BytesIO

#pip install keyboard pyautogui opencv-python numpy Pillow pyperclip

def record_screen():
    # 錄製螢幕
    frames = []
    for _ in range(60):  # 2秒 * 30幀/秒 = 60幀
        img = pyautogui.screenshot()
        frames.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        cv2.waitKey(33)  # 等待約33毫秒，實現30fps
    
    # 保存為視頻
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('temp_video.mp4', fourcc, 30, (width, height))
    for frame in frames:
        video.write(frame)
    video.release()

def convert_to_gif():
    # 將視頻轉換為GIF
    if not os.path.exists('out'):
        os.makedirs('out')
    
    clip = cv2.VideoCapture('temp_video.mp4')
    frames = []
    while True:
        ret, frame = clip.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame_rgb))
    
    output_path = os.path.join('out', 'output.gif')
    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, duration=33)
    clip.release()
    
    # 清理臨時文件
    os.remove('temp_video.mp4')
    
    return output_path

def copy_to_clipboard(file_path):
    # 將GIF複製到剪貼板
    with open(file_path, 'rb') as f:
        data = f.read()
    
    output = BytesIO(data)
    image = Image.open(output)
    
    output = BytesIO()
    image.save(output, format='GIF')
    data = output.getvalue()
    
    pyperclip.copy(data)

def main():
    print("按下 Ctrl+Alt+R 開始錄製...")
    keyboard.wait('ctrl+alt+r')
    
    print("開始錄製...")
    record_screen()
    
    print("轉換為GIF...")
    gif_path = convert_to_gif()
    
    print("複製到剪貼板...")
    copy_to_clipboard(gif_path)
    
    print("完成！GIF已保存到", gif_path, "並複製到剪貼板。")

if __name__ == "__main__":
    main()