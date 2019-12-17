# -*- coding: utf-8 -*-
#外部からシリアル通信で送られてきたEEGdataをグラフ表示するプログラム
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import serial
import sys
import math

def main():
    ser = serial.Serial("/dev/cu.usbserial", 57600, timeout=1)
    delta_waves = [0]*100
    theta_waves = [0]*100
    low_alpha_waves = [0]*100
    high_alpha_waves = [0]*100
    low_beta_waves = [0]*100
    high_beta_waves = [0]*100
    low_gamma_waves = [0]*100
    mid_gamma_waves = [0]*100
    meditations = [0]*100

    t = np.arange(0, 100, 1)

    plt.ion()#interactiveモード
    
    #Pygame(グラフィック描画ライブラリ?)の設定
    pygame.init()
    screen = pygame.display.set_mode((200, 200))#画面作成(100*100)
    pygame.display.set_caption("EEG Data") #タイトルバー
    font = pygame.font.Font(None, 30) #文字の設定

    while True:#無限ループ
        
        while True:
            try:
                data = ser.readline().decode('utf-8').rstrip() #\nまで読み込む(\nは削除される)
                #print(data)
                (delta_wave, theta_wave, low_alpha_wave, high_alpha_wave, low_beta_wave, high_beta_wave, low_gamma_wave, mid_gamma_wave) = data.split(",")
                break
            except ValueError:
                delta_wave = 0
                theta_wave = 0
                low_alpha_wave = 0
                high_alpha_wave = 0
                low_beta_wave = 0
                high_beta_wave = 0
                low_gamma_wave = 0
                mid_gamma_wave = 0

#       0~1の間はストレス高い、1以上はリラックスしている。
        meditation =(float(low_alpha_wave)+float(high_alpha_wave))/(float(low_beta_wave)+float(high_beta_wave))

        delta_waves.pop(99)
        delta_waves.insert(0,float(delta_wave))
        theta_waves.pop(99)
        theta_waves.insert(0,float(theta_wave))
        low_alpha_waves.pop(99)
        low_alpha_waves.insert(0,float(low_alpha_wave))
        high_alpha_waves.pop(99)
        high_alpha_waves.insert(0,float(high_alpha_wave))
        low_beta_waves.pop(99)
        low_beta_waves.insert(0,float(low_beta_wave))
        high_beta_waves.pop(99)
        high_beta_waves.insert(0,float(high_beta_wave))
        low_gamma_waves.pop(99)
        low_gamma_waves.insert(0,float(low_gamma_wave))
        mid_gamma_waves.pop(99)
        mid_gamma_waves.insert(0,float(mid_gamma_wave))
        meditations.pop(99)
        meditations.insert(0,float(meditation))
              
        #グラフ表示設定
        plt.clf()#画面初期化
#        line, = plt.plot(t, delta_waves, 'r-', label="delta")
#        line, = plt.plot(t, theta_waves, 'g-', label="theta")
#        line, = plt.plot(t, low_alpha_waves, 'b-', label="low_alpha")
#        line, = plt.plot(t, high_alpha_waves, 'c-', label="high_alpha")
#        line, = plt.plot(t, low_beta_waves, 'm-', label="low_beta")
#        line, = plt.plot(t, high_beta_waves, 'y-', label="high_beta")
#        line, = plt.plot(t, low_gamma_waves, 'k-', label="low_gamma")
#        line, = plt.plot(t, mid_gamma_waves, linestyle = 'solid', color = 'purple', label="mid_gamma")
              
        line, = plt.plot(t, meditations, linestyle = 'solid', color = 'lawngreen', label = 'meditation')
#        line.set_ydata(delta_waves)
#        line.set_ydata(theta_waves)
#        line.set_ydata(low_alpha_waves)
#        line.set_ydata(high_alpha_waves)
#        line.set_ydata(low_beta_waves)
#        line.set_ydata(high_beta_waves)
#        line.set_ydata(low_gamma_waves)
#        line.set_ydata(mid_gamma_waves)
        line.set_ydata(meditations)
        plt.title("Real-time EEG wave data")
        plt.xlabel("Time [s]")
        plt.ylabel("EEG wave datas")
        plt.legend() #凡例表示
        plt.grid()#グリッド表示
        plt.xlim([1,100])
#        plt.ylim([0, 50000])
#        plt.ylim([0,5])
        plt.ylim([-10,10])
        plt.draw()
        plt.pause(0.05)
              
        #Pygameの処理
        screen.fill((0,0,0))
        text = font.render("EEGdata", False, (255,255,255))
        screen.blit(text, (10,10))
        pygame.display.flip()
 
        for event in pygame.event.get():
            #終了ボタンが押されたら終了処理
            if event.type == QUIT:
                pygame.quit()
                ser.close()
                plt.close()
                sys.exit()

if __name__ == '__main__':
    main()
