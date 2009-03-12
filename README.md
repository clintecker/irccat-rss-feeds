RSS Feeds for irccat
====================

Start irccat somewhere, and invoke this script as follows:

./irccat-rss.py --feed FEED_URL [--channels CHANNEL_LIST] [--prefix PREFIX] [--host HOST] [--port PORT] [--netcat-binary NCBIN] [--netcat-options NCOPTS] &

* CHANNEL_LIST defaults to "#*" or all connected channels
* PREFIX defaults to blank
* HOST defaults to 127.0.0.1
* POST defaults to 12345
* NCBIN defaults to /bin/netcat -- Note on OS X you should specify --netcat-binary /usr/bin/nc
* NCOPTS defaults to blank. On Linux style system you may want to specify "-q 1" or "-q0"

### Examples ###

* `./irccat-rss.py --feed http://search.twitter.com/search.atom?q=apple+event --channels \#appleevent --prefix "Mar 17 Event" &`
* `./irccat-rss.py --feed http://feeds.arstechnica.com/arstechnica/everything.xml --channels \#mychan --prefix "Everything Feed" -n /usr/bin/nc --port 12346 &`
* `./irccat-rss.py --feed http://feeds.arstechnica.com/arstechnica/everything.xml --channels \#mychan,\#yourchan2,@joeschmoe`
* `./irccat-rss.py --feed http://feeds.arstechnica.com/arstechnica/everything.xml --channels \#mychan --prefix "Everything Feed" -n /usr/bin/nc -o "-q0" --port 12346 &`
