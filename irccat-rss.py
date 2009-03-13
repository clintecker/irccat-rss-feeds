#!/usr/bin/env python
import feedparser, time, sys, os, urllib
from optparse import OptionParser

def printout(s, channels, host, port, ncbin, ncopts):
  s = s.replace('"', '\"')
  s = s.replace('\n', ' ')
  try:
    out = '/bin/echo "%s %s" | %s %s %s %s' % (channels,s, ncbin, ncopts, host, port)
    print out
    o = os.popen(out).read()
  except:
    print "Error sending output"
    return
    
def tinyurl(long_url):
  return urllib.urlopen('http://tinyurl.com/api-create.php?url=%s' % long_url).read()
  
def main(feed, channels, prefix, host, port, ncbin, ncopts):
  printout("Restarted, piping from %s to %s" % (feed, channels), channels, host, port, ncbin, ncopts)
  e = {}
  c = 0
  d = feedparser.parse(feed)
  for entry in d['entries']:
    if entry.guid not in e.keys():
      c += 1
      e[entry.guid] = entry
  printout('preloaded %s items' % (c,), channels, host, port, ncbin, ncopts)
  while 1:
    time.sleep(10)
    d = feedparser.parse(feed)
    for entry in d['entries']:
      if entry.guid not in e.keys():
        e[entry.guid] = entry
        printout("%s: %s - %s" % (prefix, entry.title, tinyurl(entry.link)), channels, host, port, ncbin, ncopts)
      
if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-f", "--feed", dest="feed",
                    help="The URL of the RSS/Atom/XML Feed")
  parser.add_option("-c", "--channels",
                    dest="channels", default="#*", help="A channel or list of channels: #mychan or #mychan1,#mychan2,@joeblow")
  parser.add_option("-p", "--prefix", default="",
                    dest="prefix", help="A descriptive string to print before the entry title")
  parser.add_option("-H", "--host",
                    dest="host", default="127.0.0.1", help="The hostname or IP address of the server running irccat bot")
  parser.add_option("-P", "--port",
                    dest="post", default="12345", help="The port that the irccat bot is running on")
  parser.add_option("-n", "--netcat-binary",
                    dest="ncbin", default="/bin/netcat", help="Location and name of netcat binary")
  parser.add_option("-o", "--netcat-options",
                    dest="ncopts", default="", help="Additional options to send to netcat")
  

  (options, args) = parser.parse_args()
  
  main(feed=options.feed,channels=options.channels,prefix=options.prefix,host=options.host,port=options.post,ncbin=options.ncbin,ncopts=options.ncopts)
