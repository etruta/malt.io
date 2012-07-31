import cgi
import settings
import webapp2

from models.userprefs import UserPrefs
from util import render
from webapp2_extras.appengine.users import login_required


class ProfileHandler(webapp2.RequestHandler):
    """
    Profile settings request handler. This handles requests to view and modify
    the profile settings of a logged in user. It is invoked via URLs like:

        /profile

    """
    @login_required
    def get(self):
        """
        Render the profile settings page with the currently logged-in user's
        profile settings.
        """
        render(self, 'profile.html', {
            'success': self.request.get('success')
        })

    def post(self):
        """
        Update the currently logged-in user's profile settings, such as the
        username and email.
        """
        name = cgi.escape(self.request.get('name'))
        email = cgi.escape(self.request.get('email'))

        # Do not save unless validated - this should never happen
        # as validation happens on the page via javascript. If it does,
        # then just redirect to the profile URL
        if not name or len(name) < 4 or name in settings.RESERVED_USERNAMES:
            return webapp2.redirect('/profile')

        # Set the values and save to the data store
        user = UserPrefs.get()
        user.name = name
        user.email = email
        user.put()

        # Redirect to show a success message to the user
        return webapp2.redirect('/profile?success=1')
