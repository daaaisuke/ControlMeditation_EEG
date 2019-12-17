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

    mmp_meditations = [0]*100

    theta_waves = [0]*100
    beta_stresses = [0]*100
    theta_wave = 0
    low_alpha_wave = 0
    high_alpha_wave = 0
    low_beta_wave = 0
    high_beta_wave = 0

    self_raw_powers = [0]*100
    self_mid_alpha_waves = [0]*100
    alpha_stresses = [0]*100
    self_theta_wave = 0
    self_low_alpha_wave = 0
    self_mid_alpha_wave = 0
    self_high_alpha_wave = 0
    self_low_beta_wave = 0
    self_high_beta_wave = 0


    raw_count = 0
    raw_powers = [0]*512
    raw_powers_abs = [0]*512
    N = 512

    writerTrigger = 0
    write_matrix = [0,0,0,0,0,0]#[mid_alpha,alpha_stress,beta_stress,MMP_meditation,raw_power,theta]

    t = np.arange(0, 100, 1)
    plt.ion()#interactiveモード

    #Pygame(グラフィック描画ライブラリ?)の設定
    pygame.init()
    screen = pygame.display.set_mode((200, 200))#画面作成(100*100)
    pygame.display.set_caption("EEG Data") #タイトルバー
    font = pygame.font.Font(None, 30) #文字の設定

    #csv 書き込み設定
    f = open('./../../csv/EEG/EEGLog'+str(datetime.datetime.today())+'.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    #while True:#無限ループ
    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        if not packets:
            continue
        for p in packets:
            if isinstance(p, thinkgear.ThinkGearRawWaveData):
                raw_powers[raw_count] = p.value*1.8/4096/2000
                raw_powers_abs[raw_count] = abs(p.value*1.8/4096/2000)
                raw_count += 1
                if(raw_count >= N):

                    raw_power = round(sum(raw_powers_abs)/len(raw_powers_abs)*1000000, 2)
                    self_raw_powers.pop(99)
                    self_raw_powers.insert(0,float(raw_power))
                    write_matrix[4] = raw_power


                    F = np.fft.fft(raw_powers)
                    Amp = np.abs(F)/(N/2)

                    #self_theta_wave = round(np.sum(Amp[4:7])*10000000, 2)
                    self_low_alpha_wave = round(np.sum(Amp[7:9])*100000000, 2)
                    self_mid_alpha_wave = round(np.sum(Amp[9:11])*100000000, 2)
                    self_high_alpha_wave = round(np.sum(Amp[11:13])*100000000, 2)
                    self_low_beta_wave = round(np.sum(Amp[13:17])*100000000, 2)
                    self_high_beta_wave = round(np.sum(Amp[17:33])*100000000, 2)

                    alpha_stress = round(self_mid_alpha_wave/(self_low_alpha_wave+self_mid_alpha_wave+self_high_alpha_wave+self_low_beta_wave+self_high_beta_wave)*100, 2)
                    write_matrix[0] = self_mid_alpha_wave
                    write_matrix[1] = alpha_stress

                    beta_stress = round((self_low_alpha_wave+self_mid_alpha_wave+self_high_alpha_wave)/(self_low_beta_wave+self_high_beta_wave)*100,2)
                    write_matrix[2] = beta_stress

                    self_mid_alpha_waves.pop(99)
                    self_mid_alpha_waves.insert(0,float(self_mid_alpha_wave))
                    alpha_stressees.pop(99)
                    alpha_stresses.insert(0,float(alpha_stress))
                    beta_stresses.pop(99)
                    beta_stresses.insert(0,float(beta_stress))

                    raw_count = 0

            if isinstance(p, thinkgear.ThinkGearPoorSignalData):
                #continue
                print('Poor Signal = ' + str(p.value))

            if isinstance(p, thinkgear.ThinkGearAttentionData):
                continue
                #write_matrix[4] = p.value
            if isinstance(p, thinkgear.ThinkGearMeditationData):
                #continue
                mmp_meditation = p.value
                mmp_meditations.pop(99)
                mmp_meditations.insert(0,float(mmp_meditation))
                write_matrix[3] = mmp_meditation

            if isinstance(p, thinkgear.ThinkGearEEGPowerData):
                '''Eight EEG band power values (0　to 16777215)'''
                theta_wave, low_alpha_wave, high_alpha_wave, low_beta_wave, high_beta_wave = p.value.theta,p.value.lowalpha,p.value.highalpha,p.value.lowbeta,p.value.highbeta
                #beta_stress = round((float(low_alpha_wave)+float(high_alpha_wave))/(float(low_beta_wave)+float(high_beta_wave))*10, 2)

                #write_matrix[2] = beta_stress
                write_matrix[5] = theta_wave/100
                writerTrigger = 1

                #beta_stresses.pop(99)
                #beta_stresses.insert(0,float(beta_stress))
                theta_waves.pop(99)
                theta_waves.insert(0,float(theta_wave/100))


            #グラフ表示設定
                plt.clf()#画面初期化
                plt.subplots_adjust(wspace=0.2, hspace=0.4)

                #plt.subplot(3,2,1)
                #line, = plt.plot(t, self_mid_alpha_waves, linestyle ='solid', color = 'red',label = 'mid_alpha')
                #line.set_ydata(self_mid_alpha_waves)
                #plt.title("mid_alpha")
                #plt.xlabel("Time [s]")
                #plt.ylabel("EEG wave datas")
                #plt.legend()
                #plt.grid()
                #plt.xlim([1,100])
                #plt.ylim([0,100])

                #plt.subplot(3,2,2)
                plt.subplot(3,1,1)
                #line, = plt.plot(t, theta_waves, 'g-', label="theta")
                line, = plt.plot(t, alpha_stresses, linestyle = 'solid', color = 'orange', label = "mid_" + r'$\alpha$' +" Stress Value")

                line.set_ydata(alpha_stresses)

                plt.title("mid_" + r'$\alpha$' +" Stress Value")
                plt.xlabel("Time [s]")
                plt.ylabel("Stress")
                plt.legend() #凡例表示
                plt.grid()#グリッド表示
                plt.xlim([1,100])
                plt.ylim([0,30])

                #plt.subplot(3,2,3)
                #line, = plt.plot(t, theta_waves, linestyle ='solid', color = 'orange',label = 'theta_wave')
                #line.set_ydata(theta_waves)
                #plt.title("theta_wave")
                #plt.xlabel("Time [s]")
                #plt.ylabel("EEG wave datas")
                #plt.legend()
                #plt.grid()
                #plt.xlim([1,100])
                #plt.ylim([0,2000])

                #plt.subplot(3,2,4)
                plt.subplot(3,1,2)
                line, = plt.plot(t, beta_stresses, linestyle ='solid', color = 'lawngreen',label = r'$\alpha$' +"/"+ r'$\beta$' +" Stress Value")
                line.set_ydata(beta_stresses)
                plt.title(r'$\alpha$' +"/"+ r'$\beta$' +" Stress Value")
                plt.xlabel("Time [s]")
                plt.ylabel("Stress")
                plt.legend()
                plt.grid()
                plt.xlim([1,100])
                plt.ylim([-1,50])

                #plt.subplot(3,2,5)
                plt.subplot(3,1,3)
                line, = plt.plot(t, self_raw_powers, linestyle ='solid', color = 'skyblue',label = 'raw_value_ave')
                line.set_ydata(self_raw_powers)
                plt.title("raw_value_Avg")
                plt.xlabel("Time [s]")
                plt.ylabel("raw_value_Avg")
                plt.legend()
                plt.grid()
                plt.xlim([1,100])
                plt.ylim([0,30])


                #plt.subplot(3,2,6)
                #line, = plt.plot(t, mmp_meditations, linestyle ='solid', color = 'lawngreen',label = 'mmp_meditation')
                #line.set_ydata(mmp_meditations)
                #plt.title("mmp_meditation")
                #plt.xlabel("Time [s]")
                #plt.ylabel("EEG wave datas")
                #plt.legend()
                #plt.grid()
                #plt.xlim([1,100])
                #plt.ylim([0,100])

                plt.draw()
                plt.pause(0.05)

                #Pygameの処理
                screen.fill((0,0,0))
                text = font.render("EEGdata", False, (255,255,255))
                screen.blit(text, (10,10))
                pygame.display.flip()

        if writerTrigger ==1:
            #print(write_matrix)
            print('raw_value_ave ='+ str(write_matrix[4]))
            writer.writerow(write_matrix)
            writerTrigger = 0

        for event in pygame.event.get():
            #終了ボタンが押されたら終了処理
            if event.type == QUIT:
                pygame.quit()
                plt.close()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    writer.writerow('change user status')
                    print('change user status')

if __name__ == '__main__':
    main()
