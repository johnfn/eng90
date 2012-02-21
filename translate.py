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
  footnote_name = match[match.find(" ") + 1 : -1]
  num = match[match.find(" ") + 1 : -1]
  footnotes[num] = "<div><b class='fn' id='f_" + footnote_name + "'>" + num + ":</b> " + process(footnotes[num]) + "</div>"
  footnotebuff += process(footnotes[num]) + "\n"
  return "<sup id='" + footnote_name + "'>" + num + "</sup>"

# Gather all footnotes.
for line in lines:
  line = line.strip()
  if line == "": continue
  if line.startswith("#"):
    footnote_num = line[1:line.find(" ")]
    if footnote_num in footnotes:
      sys.stderr.write(footnote_num)
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

header = """
<!DOCTYPE html>
<html>
<head>
<link rel='stylesheet' type='text/css' href='style.css'> </link>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script>
$(function() {
  var lowest_so_far = 0;

  function bottom_of(elem) {
    return elem.offset()['top'] + elem.height();
  }

  function by_height(a, b) {
    var a_height = bottom_of($(a));
    var b_height = bottom_of($(b));

    return (a_height < b_height ? -1 : (a_height > b_height ? 1 : 0));
  }

  $("sup").sort(by_height).each(function(index) {
    var $other = $('#' + "f_" + this.id).parent();
    $other.css('position', 'absolute');
    $other.css('top', Math.max($(this).offset()['top'], lowest_so_far));
    lowest_so_far = bottom_of($other);
    console.log(lowest_so_far);
  });
});
</script>
</head>
<body>\n"""
footer = "</body></html>"

print header + "<div class='normal'>" + html + "</div> <div class='footnote'>" + footnotebuff + "</div>" + footer

#sys.stderr.write(repr(footnotes))
