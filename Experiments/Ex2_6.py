# coding: UTF-8
import signal
import sys
import pygame
import pygame.midi
import time
import pygame.pypm

#Ctrl-Cで抜けた時用の関数
def handler(signal, frame):
    player.close()
    pygame.quit()
    sys.exit(0)

print("Ex2_6.py")
pygame.midi.init()
player = pygame.midi.Output(1, latency = 1)

#Ctrl-Cで抜けたことを検知するトリガー
signal.signal(signal.SIGINT, handler)

#.txt読み取り
f = open('./midi/Ex2_Classic.txt')
lines = f.readlines()
f.close()

time_stamp = 0
Ftime_stamp = 0
for i in range(len(lines)):
    lines[i] = lines[i].rstrip('\n').split(",")

EndTrigger = True
Stime = time.time()
while EndTrigger:
    for notes in lines:
        time_stamp += long(notes[-1])/1.5/1.8
        Ftime_stamp += long(notes[-1])/1.5/1.8
        if Ftime_stamp >= 5000:
            time.sleep(5)
            Ftime_stamp = 0

        #note_on event
        if notes[0] == 'non':
            player.write([[[0x90 + int(notes[1]),int(notes[2]),int(notes[3])],time_stamp]]) #信号ステータス,ピッチ,ベロシティ,タイムスタンプ

        #note_off event
        elif notes[0] == 'nof':
            player.write([[[0x90 + int(notes[1]),int(notes[2]),0],time_stamp]])

        #control_change event
        if notes[0] == 'cc':
            player.write([[[0xb0 + int(notes[1]),int(notes[2]),int(notes[3])],time_stamp]])

        #sysex event
        elif notes[0] == 'sy':
            data = list(map(int,notes[1:-1]))
            data.insert(0,240)
            data.append(247)
            player.write_sys_ex(time_stamp,data)

        #program_change event
        elif notes[0] == 'pc':
            player.write([[[0xc0 + int(notes[1]),int(notes[2])],time_stamp]])

        #meta_message event
        #elif notes[0] == 'mt':

            #time_signature meta_message
            #if notes[1] == 'ts':
                #player.write([[[0xFF, 0x58, 0x04,int(notes[2]),int(notes[3]),int(notes[4]),int(notes[5])], int(notes[6])]])
                #player.write_sys_ex(time_stamp,[240,255, 88, 4, 4, 4, 18,8,247])

            #key_signature meta_message
            #elif notes[1] == 'ks':
                #player.write([[[0xFF, 0x59, 0x02, int(notes[2]),int(notes[3])],int(notes[4])]])
        
            #set_tempo meta_message
            #elif notes[1] == 'st':
                #tempo_hex = hex(int(notes[2]))
                #if len(tempo_hex) == 7:
                    #tempo_hex = list(tempo_hex)
                    #tempo_hex.insert(2, '0')
                    #tempo_hex = "".join(tempo_hex)
                #tempo_hexs = [0,0,0]
                #tempo_hexs[0] = tempo_hex[2:4]
                #tempo_hexs[1] = tempo_hex[4:6]
                #tempo_hexs[2] = tempo_hex[6:8]
                #player.write([[[0xFF, 0x51, 0x03, int(tempo_hexs[0]),int(tempo_hexs[1]),int(tempo_hexs[2])], int(notes[3])]])
        
            #end_of_track meta_message
            #elif notes[1] == 'eot':
                #print('finish midi message')

        if time.time() - Stime > 60:
            EndTrigger = False
            break

player.close()
pygame.quit()
