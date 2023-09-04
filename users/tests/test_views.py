from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

class TestCustomRegisterView(TestCase):
	def test_custom_register_view_status_code(self):
		self.client = Client()
		response = self.client.get(reverse('account:register'))
		self.assertEquals(response.status_code, 200)


	def test_custom_register_view_uses_correct_template(self):
		self.client = Client()
		response = self.client.get(reverse('account:register'))
		self.assertTemplateUsed(response, "users/register.html")


	def test_if_user_is_created(self):
		self.client = Client()
		data = {"username": "gooduser", 
				"email": "good@user.com", 
				"password1": "secret_123", 
				"password2": "secret_123"}
		self.client.post(reverse('account:register'), data)
		gooduser = User.objects.get(username=data["username"])

		self.assertEquals(gooduser.username, "gooduser")


	def test_if_custom_register_view_rejects_invalid_user(self):
		self.client = Client()
		# Try to register without username
		data = {"email": "good@user.com", 
				"password1": "secret_123", 
				"password2": "secret_123"}
		self.client.post(reverse('account:register'), data)

		self.assertEquals(User.objects.count(), 0)


	def test_if_custom_register_view_redirects_to_login(self):
		self.client = Client()
		data = {"username": "baduser", 
				"email": "bad@user.com", 
				"password1": "secret_123", 
				"password2": "secret_123"}
		response = self.client.post(reverse('account:register'), data)

		self.assertRedirects(response, reverse("account:login"))
		