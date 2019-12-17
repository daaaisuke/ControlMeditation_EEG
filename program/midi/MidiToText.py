# coding: UTF-8
#SMFを読み込んでmidi信号をテキストファイルに出力

from mido import MidiFile, Message
import re


# 各トラック毎の全メッセージを表示する
def dump_track(track_obj):
    for msg in track_obj:
        msg = str(msg)

        #note_on event
        if 'note_on' in msg:
            msg = re.sub('note_on','', msg)
            msg = re.sub('channel=|note=|velocity=|time=', '', msg)
            msg = 'non' + msg.replace(' ', ',') + '\n'
            file.write(msg)

        #note_off event
        elif 'note_off' in msg:
            msg = re.sub('note_off', '', msg)
            msg = re.sub("channel=|note=|velocity=|time=", '', msg)
            msg = 'nof' + msg.replace(' ', ',') + '\n'
            file.write(msg)

        #control_change {channel control value time}
        elif 'control_change' in msg:
            msg = re.sub('control_change', '', msg)
            msg = re.sub('channel=|control=|value=|time=', '', msg)
            msg = 'cc' + msg.replace(' ', ',') + '\n'
            file.write(msg)

        #sysex {data{} time}
        elif 'sysex' in msg:
            msg = re.sub('sysex', '', msg)
            msg = re.sub('data=|time=|', '', msg)
            msg = re.sub(re.compile("[(|)]"),"",msg)
            msg = 'sy' + msg.replace(' ', ',') + '\n'
            file.write(msg)

        #program_change {channel program time}
        elif 'program_change' in msg:
            msg = re.sub('program_change', '', msg)
            msg = re.sub('channel=|program=|time=', '', msg)
            msg = 'pc' + msg.replace(' ', ',') + '\n'
            file.write(msg)

        #meta message
        elif 'meta message' in msg:
            msg = re.sub('<meta message|>', '', msg)

            #meta text
            if 'text text' in msg:
                msg = re.sub('text text=u|time=','',msg)
                msg = 'mt,tx' + msg.replace(' ',',') + '\n'
                file.write(msg)

            #meta time_signature
            elif 'time_signature' in msg:
                msg = re.sub('time_signature numerator=|denominator=|clocks_per_click=|notated_32nd_notes_per_beat=|time=','',msg)
                msg = 'mt,ts' + msg.replace(' ',',') + '\n'
                file.write(msg)

            #meta key_signature
            elif 'key_signature' in msg:
                msg = re.sub(' key_signature key=|time=','',msg)

                #各値にアクセスするためにリスト型に変換
                kslist = msg.split(' ')

                #長調,短調データの切り取り
                if 'm' in kslist[0]:
                    kslist[0] = re.sub('m', '', msg)
                    kslist.insert(1,"1")

                #音階コードを数値に変換
                if 'Cb' in kslist[0]:
                    kslist[0] = '7'
                elif 'Gb' in kslist[0]:
                    kslist[0] = '6'
                elif 'Db' in kslist[0]:
                    kslist[0] = '5'
                elif 'Ab' in kslist[0]:
                    kslist[0] = '4'
                elif 'Eb' in kslist[0]:
                    kslist[0] = '3'
                elif 'Bb' in kslist[0]:
                    kslist[0] = '2'
                elif 'F' in kslist[0]:
                    kslist[0] = '1'
                elif 'C' in kslist[0]:
                    kslist[0] = '0'
                elif 'G' in kslist[0]:
                    kslist[0] = '-1'
                elif 'D' in kslist[0]:
                    kslist[0] = '-2'
                elif 'A' in kslist[0]:
                    kslist[0] = '-3'
                elif 'E' in kslist[0]:
                    kslist[0] = '-4'
                elif 'B' in kslist[0]:
                    kslist[0] = '-5'
                elif 'F#' in kslist[0]:
                    kslist[0] = '-6'
                elif 'C#' in kslist[0]:
                    kslist[0] = '-7'

                msg = ' '.join(kslist)
                msg = 'mt,ks,' + msg.replace(' ',',') + '\n'
                file.write(msg)

            #meta set_tempo
            elif 'set_tempo' in msg:
                msg = re.sub('set_tempo tempo=|time=','',msg)
                msg = 'mt,st' + msg.replace(' ',',') + '\n'
                file.write(msg)

            #meta end_of_track
            elif 'end_of_track' in msg:
                msg = re.sub('end_of_track time=','',msg)
                msg = 'mt,eot' + msg.replace(' ',',') + '\n'
                file.write(msg)

# 全トラックの全メッセージをトラック毎に表示する
def dump_smf(midi_obj):
    for i, track in enumerate(midi_obj.tracks):
        dump_track(track)

#入力ファイル(SMF)
mid = MidiFile('./midi/Ex1_Classic.midi')
#出力ファイル(txt)
file = open('./midi/Ex1_Classic.txt', 'w')
dump_smf(mid)
