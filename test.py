import os
songs = os.listdir("songs")
for sname in songs:
    print("<hr>")
    sfile= open("songs/"+sname)
    scontent = sfile.read()
    print(scontent)
    sfile.close()
