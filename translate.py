import re
import sys
import markdown

html = ""
lines = [line[:-1] for line in open("storyraw")]
footnotes = {}
footnotebuff = ""

def process(text):
  result = markdown.markdown(text)
  return result

def footnotify(item):
  global footnotebuff
  global footnotes
  match = item.group()
  num = match[match.find(" ") + 1 : -1]
  footnotes[num] = "**" + num + ":** " + footnotes[num]
  footnotebuff += process(footnotes[num]) + "\n"
  return "<sup>" + num + "</sup>"

# Gather all footnotes.
for line in lines:
  line = line.strip()
  if line == "": continue
  if line.startswith("#"):
    footnote_num = line[1:line.find(" ")]
    if footnote_num in footnotes:
      footnotes[footnote_num] += line[line.find(" ") + 1:] + "\n\n"
    else:
      footnotes[footnote_num] = line[line.find(" ") + 1:] + "\n\n"

for line in lines:
  line = line.strip()
  if line == "": continue
  if line.startswith("#"): continue

  footnote = re.compile(r'#footnote ([^#]+)#')
  line = footnote.sub(footnotify, line)

  html += process(line) + "\n"

header = "<link rel='stylesheet' type='text/css' href='style.css'> </link>\n<body>\n"
footer = "</body>"

print header + "<div class='normal'>" + html + "</div> <div class='footnote'>" + footnotebuff + "</div>" + footer

#sys.stderr.write(repr(footnotes))
