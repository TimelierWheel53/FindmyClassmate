#
import webapp2
import jinja2
import os
import hashlib, binascii #for hashing password
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def hash_password(password):
    #Hash a password for storing
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

class User(ndb.Model):
  user_name = ndb.StringProperty(required=False)
  password = ndb.StringProperty(required=False)
  e_mail = ndb.StringProperty(required=False, default = '')
  grad_date = ndb.StringProperty(required=False, default = '')
  major = ndb.StringProperty(required=False, default = '' )

class LogIn (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('index.html')
        self.response.write(template.render())
    def post(self):
        new_user = self.request.get('username')
        new_pass = self.request.get('password')
        user = User(user_name = new_user, password = hash_password(new_pass))
        user.put()
        user_check = User.query().filter(User.user_name == new_user).fetch()
        if len(user_check) > 0:
            self.error(403)
        else:
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
        #get user info from LogIn Class
        originalUser = User.query().filter(User.user_name == new_name).fetch()[0]
        originalUser.e_mail = new_mail
        originalUser.grad_date = grad
        originalUser.major = new_major
        originalUser.put()


class Major (webapp2.RequestHandler):
    def post(self):
        template=jinja_env.get_template('majors.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/', LogIn),
    ('/home', Major),
    ('/profile', Profile),
]
, debug=True)
