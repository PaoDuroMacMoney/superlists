from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'Uma nova tarefa'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Uma nova tarefa')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'Uma nova tarefa'})

        self.assertRedirects(response, '/lists/unica/')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/unica/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item 1', list=list_)
        Item.objects.create(text='Item 2', list=list_)

        response = self.client.get('/lists/unica/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item, second_saved_item = saved_items

        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(first_saved_item.text, first_item.text)

        self.assertEqual(second_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item.text)
