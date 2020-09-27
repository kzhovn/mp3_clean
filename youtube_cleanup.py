import eyed3
import os
import re
import string

path = "/home/kira/Music"
file_list = os.fsencode(path)

for file in os.listdir(file_list):
    filename = os.fsdecode(file)
    mp3 = eyed3.load(path + "/" + filename)

    ###fix artist field (remove common extra, strip white space, capitalize)
    mp3_artist = ""
    if mp3.tag.artist is not None:
        mp3_artist = re.sub(r"(?i)(vevo)|(- Topic)|(lyrics)", "", mp3.tag.artist)
        camel_case = re.findall(r"([A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$)))", mp3_artist) #SplitThisNonsense
        mp3_artist = " ".join(camel_case)
        mp3_artist = mp3_artist.strip()


    #check if empty
    if mp3_artist:
        mp3.tag.artist = mp3_artist
    else:
        mp3.tag.artist = "Unknown"

    ###fix title (remove artist name, common extra, ' | \\ //, etc)
    mp3_title = ""
    if mp3.tag.title is not None:
        mp3_title = re.sub(f"(?i)((-\s*)?(\s+by\s+)?{mp3_artist}(\s*-)?)|((with\s+)?(on-screen\s*)?lyric[s]?)|"
                        "(vevo)|(music video)|(video)|(audio)|(official)|(\sHD)|(HQ)|\"|\||\\\\|\/\/",
                         "", mp3.tag.title)
        mp3_title = re.sub(r"(\(\s*\))|(\[\s*\])|(^\s*:)|(^\s*-)|", "", mp3_title).strip() #fix messes from above
        mp3_title = re.sub(r"\s\s+", " ", mp3_title)

    #check if empty
    if mp3_title:
        mp3.tag.title = mp3_title
    else:
        mp3.tag.title = "Unknown"

    #save
    #mp3.tag.save()
    print(f"{mp3_title}, {mp3_artist}")
