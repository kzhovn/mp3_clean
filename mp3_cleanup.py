import eyed3 #needs latest version - pip install
import os
import re
import string

dir = os.path.expanduser("~/Music")
file_list = os.fsencode(dir)

track_list = []

for file in os.listdir(file_list):
    filename = os.fsdecode(file)
    mp3 = eyed3.load(dir + "/" + filename)

    freeze_metadata = False #add "freeze" to comment metadata if I want it not to mess with the formatting
    if mp3.tag.comments:
        if mp3.tag.comments[0].text == "freeze":
            freeze_metadata = True

    if not freeze_metadata:
        ###fix artist field 
        mp3_artist = ""

        if mp3.tag.artist is not None:
            mp3_artist = re.sub(r"(?i)(vevo)|(- Topic)|(lyrics)|(music)", "", mp3.tag.artist)   #remove clutter
            mp3_artist = re.sub(r"([A-Z][a-z0-9]+(?=[A-Z]))", r"\1 ", mp3_artist)       #SplitThisNonsense
            mp3_artist = mp3_artist.split(",", 1)[0]                                    #throw away everything after comma
            mp3_artist = string.capwords(mp3_artist.strip())

        if not mp3_artist or mp3_artist == " ":
            mp3.tag.artist = "Unknown"

        ###fix title
        mp3_title = ""
        if mp3.tag.title is not None:
            mp3_artist_stripped = re.sub(r"([\+-]+)", "", mp3_artist)
            title_re = re.compile( 
                        fr"""((-\s*)?(\s+by\s+)?({re.escape(mp3_artist)}|{re.escape(mp3_artist_stripped)})(\s*-)?)| #remove artist name
                        ((with\s+)?(on[-\s]screen\s*)?lyric[s]?)|   #[with] [on-screen] lyrics"
                        (((?!^)\[.*\])|(\[.*\](^$)))|   #anything between square brackets that isn't the entire because some people have to be special and name their songs [i]
                        (vevo)|(music video)|\(.*video.*\)|(audio)|(official)|(HD)|(HQ) #words, anything in parentheses with the word video
                        |\"|\||\\\\|\/\/|\'\'|\*   #quotes, |, \\, //, '', *
                        """ , re.VERBOSE | re.IGNORECASE)
            mp3_title = re.sub(title_re, "", mp3.tag.title) #remove all the above

            #fix messes from above
            title_re_2 = re.compile(
                r"""(\(\s*\))|(\[\s*\])| #remove empty parentheses
                (^\s*(_|~|:|-))|((_|~|:|-)\s*$)| #leading and trailing 
                ((\(|\[)\s*(music)\s*(\)|\]))|(\\w\s*($|\)))
                """, re.VERBOSE | re.IGNORECASE)
            mp3_title = re.sub(title_re_2, "", mp3_title) 
            
            #standardize to (ft. ARTIST)
            mp3_title = re.sub("(feat\.)|(Ft\.)|(FT\.)", "ft.", mp3_title)
            mp3_title = re.sub(r"((?<!\()\s*ft\..*)", r" (\1)", mp3_title) #ft. in parentheses
            mp3_title = re.sub(r"ft\.(?!\s)", "ft. ", mp3_title) #space after ft.

            mp3_title = re.sub(r"\s\s+", " ", mp3_title).strip() #extra whitespace
            mp3_title = re.sub(r"\(\s", "(", mp3_title) #no extra parenthese spaces (left)
            mp3_title = re.sub(r"\s\)", ")", mp3_title) #no extra parenthese spaces (right)

        if not mp3_title or mp3_title == " ":
            mp3.tag.title = "Unknown"

        ###print & save
        if (mp3.tag.artist != mp3_artist or mp3.tag.title != mp3_title):
            print(f"{mp3_title}, {mp3_artist}")
            mp3.tag.artist = mp3_artist
            mp3.tag.title = mp3_title

            mp3.tag.save()     #COMMENT OUT TO TEST CHANGES

    track_list.append((mp3.tag.title, mp3.tag.artist))

###print duplicates (https://www.techiedelight.com/find-duplicate-items-python-list/)
visited = set()
duplicate_songs = {song for song in track_list if song in visited or (visited.add(song) or False)}
print("Duplicate songs: " + str(duplicate_songs))
