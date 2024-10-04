import os
songs = os.listdir("songs")
songs.sort()

ignoreBlankLine = False
songTitles = []

def removeChordfromLine(line):
     ret = ""
     start = line.find("[")
     if start == -1:
          return line
     end = line.find("]", start)
     ret = line[:start] + line[end+1:]
     return removeChordfromLine(ret)
     
def generateSongLine(song_name, index):
     global songTitles

     title = "1"
     content = ""
     category = "c"
     level = "l"
     add = ""

     f = open("songs/" + song_name, "rb")

     for line in f:
          line_string = str(line, 'utf-8', 'ignore')
          if line_string.startswith('{title:'):
               title = line_string[8:-3]
               songTitles.append(title)
               add += "<button class='add_%s btn small_btn' onclick='addToPlaylist(%s)'><i class='fa fa-plus'></i></button>" % (index, index)
               add += "<button class='remove_%s btn small_btn red_btn' onclick='removeFromPlaylist(%s)' style='display:none'><i class='fa fa-trash'></i></button>" % (index, index)
               #add = "<div id='addlink_%s' class='add_song' onclick=addToPlaylist(%s)>Add to Playlist</div>" % (index, index)
               #add += "<div id='added_%s' class='song_added' style='display:none'>Song added</div>" % (index)
          elif line_string.startswith('# Subject:'):
               category = line_string[10:]
          elif line_string.startswith('# Level:'):
               level = line_string[9:]
          elif not line_string.startswith('#'):
               content += removeChordfromLine(line_string)
               
     return "  <td><a href='#"+str(index)+"'>"+title+"</a></td><td style='display:none'>"+content+"</td><td>"+category+"</td><td>"+level+"</td><td>"+add+"</td>"

def generateChordLine(line):
     global ignoreBlankLine

     if len(line) < 3:
          if ignoreBlankLine:
               ignoreBlankLine = False
               return ""
          else:
               return "<div class=line>&nbsp;</div>"

     if line.startswith('{'):
          return ""
     
     if line.startswith('('):
          return "<div class=note>" + line + "</div>"

     line = line.replace(" ", "&nbsp;")
     
     ret = "<div class=line>"

     # if the entire line doesn't start with a chord
     if line[0] != "[":
          ret += "<div class='section'>"

          # if no chords at all, then only include words div
          if line.find("[") == -1:
               ret += "<div class='words'>" + line
          # else, include blank chords div
          else:
               ret += "<div class='chord'>&nbsp;</div>"
               ret += "<div class='words'>" + line[:line.find("[")]
               # jump to next chord
               line = line[line.find("["):]
          ret += "</div></div>"

     # while loop for each section
     while len(line) > 0 and line.find("[") >= 0:
          ret += "<div class='section'>"

          # chord
          ret += "<div class='chord'>" + line[1:line.find("]")] + "</div>"

          line = line[line.find("]")+1:]

          # words
          ret += "<div class='words'>"
          # if the line ends with a chord, aka no more words in the line
          if len(line) == 0:
               ret += "&nbsp;"
          else:
               # if no more chords
               if line.find("[") == -1:
                    ret += line
               else:
                    ret += line[:line.find("[")]
                    # jump to next chord
                    line = line[line.find("["):]
          ret += "</div>"

          # end section
          ret += "</div>"

     # end line
     ret += "</div>"
     return ret

def generateSongContent(s_name, index):
     global ignoreBlankLine
     
     ret = "<a id=%s></a><hr>" % (index)
     ret += "<button class='add_%s btn' onclick='addToPlaylist(%s)'><i class='fa fa-plus'></i> Add to Playlist</button>" % (index, index)
     ret += "<button class='remove_%s btn red_btn' onclick='removeFromPlaylist(%s)' style='display:none'><i class='fa fa-trash'></i> Remove</button>" % (index, index)

     f = open("songs/" + s_name, "rb")

     for line in f:
          line_string = str(line, 'utf-8', 'ignore')
          if not line_string.startswith('#'):
               if line_string.startswith("{title:"):
                    ret += "<div class=song id='song_%s'><div class=title>%s</div>" % (index, line_string[8:-3])
                    ignoreBlankLine = True
               else:
                    ret += generateChordLine(line_string)
          else:
               ignoreBlankLine = True

     ret += "</div>" 

     f.close()

     return ret

def generateSongDictionary():
     global songTitles
     ret = "<script>var song_dict=["
     for s in songTitles:
          ret += "'" + s.replace("'", "\\'") + "', "
     ret += "];</script>"
     return ret


f = open("index.html", "w+")
f.write("<html>")
f.write("<head><title>Church In Anaheim Children's Songs</title><link rel='stylesheet' href='song_styles.css'/>")
f.write("<link rel='stylesheet' href='Datatables-1.10.20/css/jquery.dataTables.min.css'/>")
f.write("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'/>")
f.write("<script src='jquery-3.3.1/jquery-3.3.1.min.js'></script>")
f.write("<script src='Datatables-1.10.20/js/jquery.dataTables.min.js'></script>")
f.write("<script src='song.js'></script>")
f.write("</head><body>");
f.write("<div class=menu><div style='float:left;' onclick='showAllSongs();'>All Songs</div>")
f.write("<div id=pl_link style='float:right;' onclick='showPlaylist();'>My Playlist (0)</div></div>");
f.write("<div id=all_songs><table id=song_index class='display' style='width: 100%'> <thead>");
f.write("   <tr>")
f.write("       <th>Title</th><th>content</th><th>Category</th><th>Level</th><th></th>")
f.write("   </tr></thead><tbody>")

index = 0
for s in songs:
     f.write("<tr>")
     f.write(generateSongLine(s, index))
     index += 1
     f.write("</tr>\n")
f.write("</tbody></table><br><br><br>")

index = 0
for s_name in songs:
     f.write(generateSongContent(s_name, index))
     index += 1

f.write("</div><div id=playlist style='display: none'><table id='playlist_table' class='display' width='100%'></table><div id=playarea></div>")
f.write("</div>" + generateSongDictionary() + "<div id=toTopButton class='btn top'><i class='fa fa-arrow-up'></i> Top</div></body></html>")
f.close()
