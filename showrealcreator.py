import glob, os, time, itertools, sys, csv
from moviepy.editor import *
#from moviepy.config import change_settings
#change_settings({"IMAGEMAGICK_BINARY": "/usr/local/bin/convert"})

Filetype = "*.mp4"
Folder = "video"
dataList = "video2.list"
outFile = "test.mp4"

giftFiles = [glob.glob(str(Folder+"\\"+Filetype))]
toMerge = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

with open(dataList, newline='') as csvfile:
    lineReader = csv.reader(csvfile, delimiter='|', skipinitialspace=True)
    for row in lineReader:
        if "#" in row[0]:
            continue
        toMerge.append(row)

clips = []
dirname = os.path.dirname(__file__)

def color_clip(size, duration, text, fps=25):
    txt_background = ColorClip(size, (0,0,0), duration=duration)
    txt_clip = TextClip(text, fontsize = 75, color = 'white', font = "Amiri-Bold")
    txt_clip = txt_clip.set_pos('center').set_duration(duration)
    return CompositeVideoClip([txt_background, txt_clip])

def title_clip(size, duration, text, fps=25):
    #txt_background = ColorClip(size, (0,0,0), duration=duration)
    txt_clip = TextClip(text, fontsize = 50, color = 'white', font = "Amiri-Bold", bg_color = 'gray')
    txt_clip = txt_clip.set_pos('bottom').set_duration(duration)
    return txt_clip

#clips.append(color_clip((1280,720), 5.5, "Актёрский шоурил.\nМарина Цуркова."))
for i in range(len(toMerge)):
    inputFile = os.path.join(dirname, Folder, toMerge[i][0])
    print(bcolors.OKBLUE + "Open video: "+ inputFile + bcolors.ENDC)
    title = str(toMerge[i][1])
    if len(toMerge[i]) > 2:
         title += "\n" + str(toMerge[i][2])
    #clips.append(color_clip((1280,720), 5, title))
    #clips.append(VideoFileClip(inputFile))
    background_clip = ColorClip((1280,720), (0,0,0), duration=VideoFileClip(inputFile).duration)
    #clips.append(CompositeVideoClip([background_clip, VideoFileClip(inputFile).resize(height=720).set_pos('center'),title_clip((1280,720), VideoFileClip(inputFile).duration, title)]))
    if i == 0:
        clips.append(CompositeVideoClip([VideoFileClip(inputFile).resize(height=720).set_pos('center'),title_clip((1280,720), VideoFileClip(inputFile).duration, title),color_clip((1280,720), 6, "Актёрский шоурил.\nМарина Цуркова.")]))
    else:
        clips.append(CompositeVideoClip([background_clip, VideoFileClip(inputFile).resize(height=720).set_pos('center'),title_clip((1280,720), VideoFileClip(inputFile).duration, title)]))

newClip = concatenate_videoclips(clips)
newClip.write_videofile(outFile, audio_codec="aac")
newClip.close()

for i in range(len(clips)):
    clips[i].close()
