from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

class CustomSessionMiddleware(SessionMiddleware):

    def process_response(self, request, response):
        response = super(CustomSessionMiddleware, self).process_response(request, response)
        #You have access to request.user in this method
        if not request.user.is_authenticated:
            response.delete_cookie(settings.SESSION_COOKIE_NAME)
        return response