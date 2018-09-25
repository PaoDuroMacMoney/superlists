from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        first_list = List.objects.create()
        second_list = List.objects.create()

        self.client.post(
                f'/lists/{first_list.id}/add_item',
                data={'item_text': 'Novo item para lista existente'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Novo item para lista existente')
        self.assertEqual(new_item.list, first_list)
    
    def test_redirects_to_list_view(self):
        outra = List.objects.create()
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/add_item',
            data={'item_text':'Novo item'})
        
        self.assertRedirects(response, f'/lists/{list_.id}/')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'Uma nova tarefa'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Uma nova tarefa')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'Uma nova tarefa'})
        list_ = List.objects.first()

        self.assertRedirects(response, f'/lists/{list_.id}/')


class ListViewTest(TestCase):
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_uses_list_template(self):
        list_ = List.objects.create()

        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


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
