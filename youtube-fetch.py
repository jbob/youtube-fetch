#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import feedparser
import datetime

USER = sys.argv[1]
URL = 'http://gdata.youtube.com/feeds/base/users/'+USER+'/newsubscriptionvideos'
DOWNLOADDIR = '/home/markus/platte1000/downloads/youtube/'

class Downloaded:
  def __init__(self, dbfile=DOWNLOADDIR+'.dbfile.txt'):
    self.dbfile = dbfile
    db = file
    try:
      db = open(self.dbfile)
    except IOError:
      db = open(self.dbfile, 'w')
      db.close()
      db = open(self.dbfile)

    self.downloaded = []
    for line in db:
      self.downloaded.append(line.strip())
    db.close()

  def get(self, link):
    if link in self.downloaded:
      return True
    else:
      return False

  def add(self, link):
    self.downloaded.append(link)
    db = open(self.dbfile, 'w')
    db.write('\n'.join(self.downloaded))
    db.close()

def main():
  init = False
  if len(sys.argv) > 2 and sys.argv[2] == 'init':
    # Initialize. Don't download anything, just mark every video 
    # in the feed as seen.
    init = True


  downloaded = Downloaded()
  # First delte old files
  files = os.listdir(DOWNLOADDIR)
  for f in files:
    modified = datetime.datetime.fromtimestamp(os.path.getmtime(DOWNLOADDIR+f))
    if (datetime.datetime.now() - modified) > datetime.timedelta(days=14):
      os.remove(DOWNLOADDIR+f)

  # Get current feed and download new videos
  feed = feedparser.parse(URL)
  for entry in feed.entries:
    link = entry.link
    if not downloaded.get(link):
      if init == False:
        print "Downloading:", link
        result = subprocess.call(['youtube-dl', '-c', '-o', DOWNLOADDIR+'%(upload_date)s_%(stitle)s_%(uploader)s.avi', link])
        if result == 0:
          print "Download successfull"
          downloaded.add(link)
        else:
          print "Fehler"
          exit(1)
      else:
        downloaded.add(link)
    else:
      print "Skipping:", link


if __name__ == '__main__':
  main()
