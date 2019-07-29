#
import webapp2
import jinja2
import os
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class User(ndb.Model):
  name = ndb.StringProperty(required=True)
  password = ndb.StringProperty(required=True)


class LogIn (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('index.html')
        self.response.write(template.render())
    def post(self):
        new_user = self.request.get('newname')
        new_pass = self.request.get('newpass')
        user = User(name = new_user,
                    password = new_pass)
        user.put()

#class Home (webapp2.RequestHandler):


class Profile (webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('profile.html')
        self.response.write(profile_template.render())


application = webapp2.WSGIApplication([
    ('/', LogIn),
    #('/home', Home ),
    ('/profile', Profile),
]
, debug=True)
