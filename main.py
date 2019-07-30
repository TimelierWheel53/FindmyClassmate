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
  user_name = ndb.StringProperty(required=False, default= '')
  password = ndb.StringProperty(required=False, default = '')
  e_mail = ndb.StringProperty(required=False, default = '')
  grad_date = ndb.StringProperty(required=False, default = '')
  major = ndb.StringProperty(required=False, default = '' )

class LogIn (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('index.html')
        self.response.write(template.render())
    def post(self):
        new_user = self.request.get('newname')
        new_pass = self.request.get('newpass')
        user = User(user_name = new_user,
                    password = new_pass)
        user.put()
        self.redirect("/profile")

class Profile (webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('profile.html')
        self.response.write(profile_template.render())
    def post(self):
        new_name = self.request.get('name')
        new_mail = self.request.get('email')
        grad = self.request.get('grad')
        new_major = self.request.get('major')
        user = User(e_mail = new_mail,
                    grad_date = grad,
                    major = new_major,)
        user.put()

class Major (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('majors.html')
        self.response.write(template.render())



application = webapp2.WSGIApplication([
    ('/', LogIn),
    ('/home', Major),
    ('/profile', Profile),
]
, debug=True)
