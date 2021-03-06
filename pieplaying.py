#
# PieVideoPlayer
# Copyright (C) 2015 James D, Terry
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from omxplayer import OMXPlayer
import shelve
import os
from time import sleep

def main():
    play_video()
    play_video()

def play_video():
    db = shelve.open('datastore', 'c')

    video_index = db.get('video_index', 0)
    videos = db.get('videos', [])

    if video_index >= len(videos):
        video_index = 0

    if video_index >= len(videos):
        return

    db['video_index'] = video_index
    db.close()

    print "play " + videos[video_index]

    videofile = os.path.abspath(os.getcwd()) + "/video/" + videos[video_index]

    print videofile

    player = OMXPlayer(videofile, args=['--no-osd', '--no-keys', '-b'])

    player.play()

    while 1:
        try:
            print player.playback_status()
        except:
            print "error end"
            player.quit()
            return
        
def inc_video_index():
    db = shelve.open('datastore', 'c')

    video_index = db.get('video_index', 0)
    videos = db.get('videos', [])

    video_index = video_index + 1

    db['video_index'] = video_index
    db.close()

if __name__ == '__main__':
    main()
