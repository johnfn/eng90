import re
import markdown

html = ""
lines = [line[:-1] for line in open("storyraw")]
footnotes = {}
footnotebuff = ""

def process(text):
  result = markdown.markdown(text)
  return result[3:-4]

def footnotify(item):
  global footnotebuff
  global footnotes
  match = item.group()
  num = match[match.find(" ") + 1 : -1]
  footnotebuff += "<div class='footnote'>" + process(footnotes[num]) + "</div>"
  return ""

for line in lines:
  line = line.strip()
  if line == "": continue
  if line.startswith("#"):
    footnotes[line[1:line.find(" ")]] = line[line.find(" ") + 1:]
    continue

  footnote = re.compile(r'#footnote (\d+)#')
  line = footnote.sub(footnotify, line)
  if footnotebuff != "":
    html += footnotebuff + "\n"

  html += "<div class='normal'>" + process(line) + "</div>\n"

  footnotebuff = ""

header = "<link rel='stylesheet' type='text/css' href='style.css'> </link>\n<body>\n"
footer = "</body>"

print header + html + footer
