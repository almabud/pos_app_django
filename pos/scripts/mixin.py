from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.shortcuts import redirect


class LoggedOutRequiredMixin(UserPassesTestMixin):
    redirect_url = None

    def get_redirect_url(self):
        """
        Get the redirect url defalt is login url
        """
        redirect_url = self.redirect_url or settings.DASHBOARD_URL
        if not redirect_url:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_url attribute. Define {0}.redirect_url, settings.DASHBOARD_URL,'
                ' or override {0}.redirect_url().'.format(self.__class__.__name__)
            )
        return str(redirect_url)

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        """If test_fun return false then redirect to another page"""

        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect(self.get_redirect_url())

