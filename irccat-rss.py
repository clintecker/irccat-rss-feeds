#!/usr/bin/env python
# -*- coding: utf-8 -*-
import feedparser, time, sys, os, urllib, re
from optparse import OptionParser

def fmt_coveritlive(entry):
  return "%s: %s" % (entry.title, entry.summary)
def fmt_default(entry):
  return "%s" % (entry.title,)

fmtters = {
  'coveritlive': fmt_coveritlive,
  'default': fmt_default,
}

def break_up_message(s):
  s = s.split(' ')
  final = []
  i = 0
  j = 0
  while len(s):
    t = ''
    ta = []
    for i in range(len(s)):
      if(len(t+' '+s[i]) < 440):
        t = t + ' ' + s[i]
        ta.append(s[i])
        j += 1
      else:
        break
    final.append(" ".join(ta))
    s = s[j:]
    j = 0
  return final

def printout(s, channels, host, port, ncbin, ncopts):
  s = s.replace(u'"', u'\"')
  s = s.replace(u'\n', u' ')
  # Popen doesn't let you pass unicode, so we'll take out some common stuff
  s = s.replace(u'\xa0', '')
  s = s.replace(u'\u2014', '--')
  s = s.replace(u'&nbsp;', '')
  p = re.compile(r'<.*?>')
  s = p.sub('', s) # Remove tags
  
  s = unicode(s) # Make sure we're unicode I guess
  
  messages = break_up_message(s)
  
  try:
    for s in messages:
      out = u'/bin/echo "%s %s" | %s %s %s %s' % (channels, s, ncbin, ncopts, host, port)
      print out
      o = os.popen(out).read()
      time.sleep(1)
  except:
    print "Error sending output"
    return
    
def tinyurl(long_url):
  return urllib.urlopen('http://tinyurl.com/api-create.php?url=%s' % long_url).read()
  
def main(feed, channels, prefix, host, port, ncbin, ncopts, formatter):
  printout("Restarted, piping from %s to %s" % (feed, channels), channels, host, port, ncbin, ncopts)
  e = {}
  c = 0
  fmtter = fmtters[formatter]
  d = feedparser.parse(feed)
  for entry in d['entries']:
    try:
      guid = entry.guid
    except AttributeError:
      try:
        guid = entry.updated
      except AttributeError:
        raise
    if guid not in e.keys():
      c += 1
      e[guid] = entry
  printout('preloaded %s items' % (c,), channels, host, port, ncbin, ncopts)
  while 1:
    time.sleep(4)
    d = feedparser.parse(feed)
    for entry in d['entries']:
      try:
        guid = entry.guid
      except AttributeError:
        try:
          guid = entry.updated
        except AttributeError:
          raise
      if guid not in e.keys():
        e[guid] = entry
        try:
          link = entry.link
        except AttributeError:
          link = None
        if link:
          printout(u"%s%s - %s" % (prefix, fmtter(entry), tinyurl(entry.link)), channels, host, port, ncbin, ncopts)
        else:
          printout(u"%s%s" % (prefix, fmtter(entry)), channels, host, port, ncbin, ncopts)
      
if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-f", "--feed", dest="feed",
                    help="The URL of the RSS/Atom/XML Feed")
  parser.add_option("-c", "--channels",
                    dest="channels", default="#*", help="A channel or list of channels: #mychan or #mychan1,#mychan2,@joeblow")
  parser.add_option("-p", "--prefix", default=u"",
                    dest="prefix", help="A descriptive string to print before the entry title")
  parser.add_option("-H", "--host",
                    dest="host", default="127.0.0.1", help="The hostname or IP address of the server running irccat bot")
  parser.add_option("-P", "--port",
                    dest="post", default="12345", help="The port that the irccat bot is running on")
  parser.add_option("-n", "--netcat-binary",
                    dest="ncbin", default="/bin/netcat", help="Location and name of netcat binary")
  parser.add_option("-o", "--netcat-options",
                    dest="ncopts", default="", help="Additional options to send to netcat")
  parser.add_option("-F", "--formatter",
                    dest="formatter", default="default", help="The way you want your message formatted")

  (options, args) = parser.parse_args()
  if options.prefix != "":
    options.prefix = options.prefix + ": "
  main(feed=options.feed,channels=options.channels,prefix=options.prefix,host=options.host,port=options.post,ncbin=options.ncbin,ncopts=options.ncopts,formatter=options.formatter)
