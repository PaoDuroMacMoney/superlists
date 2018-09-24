from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):

	
	def test_defaul_returns_home_page(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

		
	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
	
	
	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'item_text': 'Uma nova tarefa'})
		self.assertIn('Uma nova tarefa', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')