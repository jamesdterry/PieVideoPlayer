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
import cherrypy
import os
import shutil
import shelve

class PieVideoPlayer(object):
    @cherrypy.expose
    def index(self):
        html = """<html><body><h1>PVP</h1><img src=\"img/pie.jpg\"/>
        <ul>
          <li><a href="list">List Videos</a></li>
          <li><a href="upload">Upload Video</a></li>
        </ul>
        </body></html>"""

        return html

    @cherrypy.expose
    def upload(self):
        html = "<html><body>"
        html = html + "Request method: "
        html = html + cherrypy.request.method
        html = html + "<br/>"
        html = html + "<form action=\"uploadfile\" method=\"post\" enctype=\"multipart/form-data\">"

        html = html + "filename: <input type=\"file\" name=\"myFile\" /><br/>"
        html = html + "<input type=\"submit\" />"
        html = html + "</form>"

        html = html + "</body></html>"
        return html

    @cherrypy.expose
    def uploadfile(self, myFile):
        db = shelve.open('datastore', 'c')

        dst = os.path.abspath(os.getcwd()) + "/video/" + myFile.filename

        with open(dst, 'wb') as dst_file:
            shutil.copyfileobj(myFile.file, dst_file)
            videos = []
            if db.has_key('videos'):
                videos = db['videos']
            if not myFile.file in videos:
                videos.append(myFile.filename)
                db['videos'] = videos

        db.close()

        out = """<html>
        <body>
            myFile filename: %s<br />
            myFile mime-type: %s
        </body>
        </html>"""

        return out % (myFile.filename, myFile.content_type)

    @cherrypy.expose
    def list(self):
        html = """<html><body><h1>Video List:</h1>
        <ul>"""

        db = shelve.open('datastore', 'c')
        videos = db.get('videos', [])

        for v in videos:
            html = html + "<li>" + v + "</li>"

        db.close()


        html = html + """</ul>
        </body></html>"""

        return html



if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './img'
        }
    }

    cherrypy.quickstart(PieVideoPlayer(), '/', conf)
