# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import thinkgear
import sys
import math
import csv
import datetime

def main():
    PORT = '/dev/tty.MindWaveMobile-SerialPo'

    #delta_waves = [0]*100
    #theta_waves = [0]*100
    #low_alpha_waves = [0]*100
    #high_alpha_waves = [0]*100
    #low_beta_waves = [0]*100
    #high_beta_waves = [0]*100
    #low_gamma_waves = [0]*100
    #mid_gamma_waves = [0]*100
    meditations = [0]*100

    delta_wave = 0
    theta_wave = 0
    low_alpha_wave = 0
    high_alpha_wave = 0
    low_beta_wave = 0
    high_beta_wave = 0
    low_gamma_wave = 0
    mid_gamma_wave = 0

    count = 0

    #-----matplotlib初期設定-----
    t = np.arange(0, 100, 1)
    plt.ion()#interactiveモード

    #-----Pygame初期設定-----
    pygame.init()
    screen = pygame.display.set_mode((200, 200))#画面作成(100*100)
    pygame.display.set_caption("EEG Data") #タイトルバー
    font = pygame.font.Font(None, 30) #文字の設定

    #-----csv 書き込み設定-----
    f = open('EEGLog'+str(datetime.datetime.today())+'.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        #-----受信なし-----
        if not packets:
            continue

        for p in packets:

            #-----データ種による判別-----
            #-----RawData-----
            if isinstance(p, thinkgear.ThinkGearRawWaveData):
                print(p.value)
                writer.writerow([p.value])

            #-----PoorSignal-----
            if isinstance(p, thinkgear.ThinkGearPoorSignalData):
                #print(p.value)
                continue

            #-----AttentionData-----
            if isinstance(p, thinkgear.ThinkGearAttentionData):
                continue

            #-----MedditationData-----
            if isinstance(p, thinkgear.ThinkGearMeditationData):
                continue

            #-----各周波数パワースペクトルデータ-----
            if isinstance(p, thinkgear.ThinkGearEEGPowerData):
                continue
                


        for event in pygame.event.get():
            #終了ボタンが押されたら終了処理
            if event.type == QUIT:
                pygame.quit()
                #ser.close()
                plt.close()
                sys.exit()

if __name__ == '__main__':
    main()
