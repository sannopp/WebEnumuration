import gtts
import pandas as pd
from pydub import AudioSegment
import os
from gtts import gTTS


def text_to_speech(text, filename):
    my_text = str(text)
    a = gTTS(text=my_text, slow=True)
    a.save(filename)


# text_to_speech('Krupya dhyan dijiye bareli se chalkar gaziyabad ke raste delhi ko jane vali Train'
#                ' 14315 enter city express kuchhahi samay me platfome number 3 par aa rahi he ', 'hello.mp3')


def generate_announcement(filename):
    df = pd.read_excel(filename)
    # print(df)
    for index, item in df.iterrows():
        s = " "
        s += " Krupya dhyan dijiye "
        s += " Train number "
        s += f" {item['Train No.']}"
        s += f" {item['Train Name']}"
        s += f" will departure from "
        s += f" {item['Origin']}"
        s += f" at "
        t = str(item['Arr.Time']).split(':')
        s += f" {t[0]} hour and {t[1]} minute "
        s += f" to "
        s += f" {item['Destination']}"
        s += f" Dropping time "
        t = str(item['Dep.Time']).split(':')
        s += f" {t[0]} hour and  {t[1]} minute "
        s += f"  average Travel Time is "
        t = str(item['Travel Time']).split(':')
        s += f" {t[0]} hour and  {t[1]} minute "
        s += f" "
        text_to_speech(s, f'{index+1}announcement.mp3')
        print(s)
    pass


if __name__ == '__main__':
    print('announcement...')
    generate_announcement('Train_Schedule.xlsx')
    # a = '11:22'
    # b = a.split(':')
    # print(b)
    pass
