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
        name_user = self.request.get('username')
        word_pass = self.request.get('password')
        user = User(name = name_user,
                    password = word_pass)
        all_users = User.query().fetch()
        all_users.insert (0,user)

application = webapp2.WSGIApplication([('/', LogIn)], debug=True)
