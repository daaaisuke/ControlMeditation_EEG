import pygame
import pygame.midi

pygame.midi.init()
screen = pygame.display.set_mode((800,128))
input_id = pygame.midi.get_default_input_id()
print("input MIDI:%d" % input_id)
midi_in = pygame.midi.Input(input_id)
print ("starting")
print ("full midi_events:[[[status,data1,data2,data3],timestamp]]")

loop = True
count = 0
while loop:
    if midi_in.poll():
        midi_events = midi_in.read(1)
        print ("full midi_events:" + str(midi_events))
        count += 1
        #print count
    if count >= 2700:
        loop = False

midi_in.close()
pygame.midi.quit()
