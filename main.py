#
import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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
        all_users = User.query().fetch()
class Profile (webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('profile.html')
        self.response.write(profile_template.render())


application = webapp2.WSGIApplication([
    ('/', LogIn),
    ('/profile', Profile),
]
, debug=True)
