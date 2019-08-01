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

def verify_password(stored_password, provided_password):
    #Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

class User(ndb.Model):
    name = ndb.StringProperty(required=False)
    user_name = ndb.StringProperty(required=False)
    password = ndb.StringProperty(required=False)
    e_mail = ndb.StringProperty(required=False, default = '')
    grad_date = ndb.StringProperty(required=False, default = '')
    major = ndb.StringProperty(required=False, default = '' )

class Home (webapp2.RequestHandler):
     def get(self):
         template=jinja_env.get_template('homepage.html')
         self.response.write(template.render())

class CreateAccount (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('index.html')
        self.response.write(template.render())
    def post(self):
        #register a new account
        print('test')
        new_user = self.request.get('newname')
        new_pass = self.request.get('newword')
        user_check = User.query().filter(User.user_name == new_user).fetch()
        if len(user_check) > 0:
            self.error(403)
        else:
            user = User(user_name = new_user, password = hash_password(new_pass))
            user.put()
            self.redirect('/profile')

class LogIn (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('login.html')
        self.response.write(template.render())
    def post(self):
        provided_username = self.request.get('username')
        provided_password = self.request.get('password')
        stored_username = User.query().filter(User.user_name == provided_username).fetch()[0]
        check_pass = verify_password(stored_username.password, provided_password)
        if check_pass == True:
            self.redirect('/home')
        else:
            self.error(404)

class Profile (webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('profile.html')
        self.response.write(profile_template.render())
    def post(self):
        new_name = self.request.get('nameuser')
        new_namename = self.request.get('name')
        new_mail = self.request.get('email')
        grad = self.request.get('grad')
        new_major = self.request.get('major')
        #get user info from LogIn Class
        originalUser = User.query().filter(User.user_name == new_name).fetch()[0]
        originalUser.e_mail = new_mail
        originalUser.grad_date = grad
        originalUser.major = new_major
        originalUser.name = new_namename
        originalUser.put()
        self.redirect('/home')

class Major (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('majors.html')
        self.response.write(template.render())
    def post(self):
        student = User.query().filter(User.user_name == 'Apple').fetch()
        student_name = student.user_name
        student_major = student.major
        dictionary = {
            "Name": student_name,
            "Major": student_major,
        }
        template=jinja_env.get_template('majors.html')
        self.response.write(template.render(dictionary))


class Snake (webapp2.RequestHandler):
    def get(self):
        template=jinja_env.get_template('snake.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/', Home),
    ('/signup', CreateAccount),
    ('/signin', LogIn),
    ('/home', Major),
    ('/profile', Profile),
    ('/snake', Snake)
]
, debug=True)
