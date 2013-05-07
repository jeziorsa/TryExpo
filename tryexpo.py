import cgi
import datetime
import urllib
import webapp2

from google.appengine.api import users

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        self.redirect('/')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blob_key):
        blob_key = str(urllib.unquote(blob_key))
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key))

class MainHandler(webapp.RequestHandler):
    def get(self):
        # upload_url = blobstore.create_upload_url('/upload')
        # self.response.out.write('<html><body>')
        # self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        # self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")
        images_list = blobstore.BlobInfo.all()


        template_values = {
            'images': images_list,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


        # for b in blobstore.BlobInfo.all():
        #     self.response.out.write('<li><img src="/serve/%s' % str(b.key()) + '">' + str(b.filename) + '</a>')

app = webapp2.WSGIApplication([('/', MainHandler), ('/upload', UploadHandler), ('/serve/([^/]+)?', ServeHandler)], debug=True)