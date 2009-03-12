#!/usr/bin/env python
import feedparser, time, sys, os, urllib

def printout(s, channels):
  s = s.replace('"', '\"')
  try:
    o = os.popen('/bin/echo "%s %s" | /bin/netcat -q 1 127.0.0.1 12345' % (channels,s)).read()
  except:
    return
    
def tinyurl(long_url):
  return urllib.urlopen('http://tinyurl.com/api-create.php?url=%s' % long_url).read()
  
def main(feed, name, channels="*#"):
  printout("Restarted, piping from %s to %s" % (feed, channels), channels)
  e = {}
  c = 0
  d = feedparser.parse(feed)
  for entry in d['entries']:
    if entry.guid not in e.keys():
      c += 1
      e[entry.guid] = entry
  printout('preloaded %s items' % (c,), channels)
  while 1:
    time.sleep(10)
    d = feedparser.parse(feed)
    for entry in d['entries']:
      if entry.guid not in e.keys():
        e[entry.guid] = entry
        printout("%s: %s - %s" % (name, entry.title, tinyurl(entry.link)), channels)
      
if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "Please provide a feed and a channel list"
    sys.exit(-5000)
  if len(sys.argv) == 4:
    name = sys.argv[3] + ": "
  else:
    name = ""
  main(feed=sys.argv[1],channels=sys.argv[2],name=name)
