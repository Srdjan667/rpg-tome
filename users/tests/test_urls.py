from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import (
    CustomLoginView,
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    CustomRegisterView,
)


class TestUsersUrls(SimpleTestCase):
    def test_custom_register_view_is_resolved(self):
        url = reverse("account:register")
        self.assertEquals(resolve(url).func, CustomRegisterView)

    def test_custom_login_view_is_resolved(self):
        url = reverse("account:login")
        self.assertEquals(resolve(url).func.view_class, CustomLoginView)

    def test_logout_view_is_resolved(self):
        url = reverse("account:logout")
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_custom_password_change_view_is_resolved(self):
        url = reverse("account:password_change")
        self.assertEquals(resolve(url).func.view_class, CustomPasswordChangeView)

    def test_password_reset_view_is_done_resolved(self):
        url = reverse("account:password_change_done")
        self.assertEquals(resolve(url).func.view_class, PasswordChangeDoneView)

    def test_custom_password_reset_view_is_resolved(self):
        url = reverse("account:password_reset")
        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetView)

    def test_password_reset_done_view_is_resolved(self):
        url = reverse("account:password_reset_done")
        self.assertEquals(resolve(url).func.view_class, PasswordResetDoneView)

    def test_custom_password_reset_confirm_view_is_resolved(self):
        url = reverse(
            "account:password_reset_confirm", args=["dummy_uidb64", "dummy_token"]
        )

        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetConfirmView)

    def test_password_reset_complete_view_is_resolved(self):
        url = reverse("account:password_reset_complete")
        self.assertEquals(resolve(url).func.view_class, PasswordResetCompleteView)
