import os
songs = [f for f in os.listdir('songs') if f.endswith('.pro')]
songs.sort()
for sname in songs:
    print("<hr>" + sname)
    #sfile= open("songs/"+sname)
    #scontent = sfile.read()
    #print(scontent)
    #sfile.close()
