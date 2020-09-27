import eyed3
import os
import re
import string

dir = os.path.expanduser("~/Music")
file_list = os.fsencode(dir)

for file in os.listdir(file_list):
    filename = os.fsdecode(file)
    mp3 = eyed3.load(dir + "/" + filename)

    ###fix artist field 
    mp3_artist = ""

    if mp3.tag.artist is not None:
        mp3_artist = re.sub(r"(?i)(vevo)|(- Topic)|(lyrics)", "", mp3.tag.artist)   #remove clutter
        mp3_artist = re.sub(r"([A-Z][a-z0-9]+(?=[A-Z]))", r"\1 ", mp3_artist)       #SplitThisNonsense
        mp3_artist = mp3_artist.split(",", 1)[0]                                    #throw away everything after comma
        mp3_artist = string.capwords(mp3_artist.strip())

    if not mp3_artist:
        mp3.tag.artist = "Unknown"

    ###fix title
    mp3_title = ""

    if mp3.tag.title is not None:
        mp3_artist_stripped = re.sub(r"([\+-]+)", "", mp3_artist)
        title_re = re.compile(
                    fr"""((-\s*)?(\s+by\s+)?({re.escape(mp3_artist)}|{re.escape(mp3_artist_stripped)})(\s*-)?)| #remove artist name
                    ((with\s+)?(on-screen\s*)?lyric[s]?)|
                    (vevo)|(music video)|(video)|(audio)|(official)|(\sHD)|(HQ)|\"|\||\\\\|\/\/
                    """ , re.VERBOSE | re.IGNORECASE)
        mp3_title = re.sub(title_re, "", mp3.tag.title) 

        mp3_title = re.sub(r"(?i)(\(\s*\))|(\[\s*\])|(^\s*:)|(^\s*-)|((\(|\[)\s*(music)\s*(\)|\]))", "", mp3_title) #fix messes from above
        mp3_title = re.sub(r"\s\s+", " ", mp3_title).strip() #extra whitespace

    if not mp3_title:
        mp3.tag.title = "Unknown"

    ###print & save
    if (mp3.tag.artist != mp3_artist or mp3.tag.title != mp3_title):
        print(f"{mp3_title}, {mp3_artist}")
        mp3.tag.artist = mp3_artist
        mp3.tag.title = mp3_title

        mp3.tag.save()     #COMMENT OUT TO TEST CHANGES
