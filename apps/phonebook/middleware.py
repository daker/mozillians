import os

from django.http import (HttpResponseForbidden, HttpResponseNotAllowed,
                         HttpResponseRedirect)

import commonware.log
from funfactory.manage import ROOT
from funfactory.urlresolvers import reverse

# TODO: this is hackish. Once we update mozillians to the newest playdoh layout
error_page = __import__('%s.urls' % os.path.basename(ROOT)).urls.error_page
log = commonware.log.getLogger('m.phonebook')


class PermissionDeniedMiddleware(object):
    """Add a generic 40x "not allowed" handler.

    TODO: Currently uses the 500.html error template, but in the future should
    display a more tailored-to-the-actual-error "not allowed" page."""
    def process_response(self, request, response):
        if isinstance(response, (HttpResponseForbidden,
                                 HttpResponseNotAllowed)):
            if request.user.is_authenticated():
                log.debug('Permission denied middleware, user was '
                         'authenticated, sending 500')
                return error_page(request, 500, status=response.status_code)
            else:
                if isinstance(response, (HttpResponseForbidden)):
                    log.debug('Response was forbidden')
                elif isinstance(response, (HttpResponseNotAllowed)):
                    log.debug('Response was not allowed')
                log.debug('Permission denied middleware, redirecting home')
                return HttpResponseRedirect(reverse('home'))
        return response
