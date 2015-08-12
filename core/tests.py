__author__ = 'vitor'

from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.db import IntegrityError
from core.models import FBUser
import json


class RestViewPostTest(TestCase):

    def test_post(self):
        #post deve retornar status code 201 e criar um registro no banco
        data = {'facebookId': '100002348657671'}
        resp = self.client.post(r('person_add_n_list'), data)
        self.assertEqual(201, resp.status_code)
        self.assertTrue(FBUser.objects.exists())

    def test_fbid_unique(self):
        #fb id deve ser unico no banco
        data = {'facebookId': '100002348657671'}
        resp = self.client.post(r('person_add_n_list'), data)
        obj = FBUser(name=u'Vitor Hugo Campos', fbid=u'100002348657671')
        self.assertRaises(IntegrityError, obj.save)

    def test_wrong_fbid(self):
        #fb id invalido deve retornar 404
        data = {'facebookId': '100002348657674'}
        resp = self.client.post(r('person_add_n_list'), data)
        self.assertEqual(404, resp.status_code)


class RestViewListTest(TestCase):

    def setUp(self):
        obj = FBUser(name=u'Vitor Hugo Campos', fbid=u'100002348657671')
        obj.save()
        obj = FBUser(name=u'Jason Montez', fbid=u'100002348657677')
        obj.save()

    def test_list(self):
        #deve retornar 200 e 2 usuarios
        resp = self.client.get(r('person_add_n_list'))
        content = json.loads(resp.content)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, len(content))

    def test_list_limit(self):
        #deve retornar somente a quantidade de usuarios passada como parametro
        resp = self.client.get(r('person_add_n_list')+'?limit=1')
        content = json.loads(resp.content)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, len(content))


class RestViewDetailTest(TestCase):

    def setUp(self):
        self.obj = FBUser(name=u'Vitor Hugo Campos', fbid=u'100002348657671')
        self.obj.save()

    def test_get(self):
        #deve retornar status code 200 e os dados do usuario
        resp = self.client.get(r('person_detail_n_delete', args=[self.obj.fbid]))
        content = json.loads(resp.content)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(u'100002348657671', content['fbid'])
        self.assertEqual(u'Vitor Hugo Campos', content['name'])

    def test_get_404(self):
        #deve retornar 404 quando tentar detalhar um zipcode que nao esta no banco
        resp = self.client.get(r('person_detail_n_delete', args=['100002348657672']))
        self.assertEqual(404, resp.status_code)


class RestViewDeleteTest(TestCase):

    def setUp(self):
        self.obj = FBUser(name=u'Vitor Hugo Campos', fbid=u'100002348657671')
        self.obj.save()

    def test_delete(self):
        #deve retornar status code 204 e deletar o registro no banco
        resp = self.client.delete(r('person_detail_n_delete', args=[self.obj.fbid]))
        self.assertEqual(204, resp.status_code)
        self.assertFalse(FBUser.objects.exists())

    def test_delete_404(self):
        #deve retornar 404 quando tentar deletar um usuario que nao esta no banco
        resp = self.client.delete(r('person_detail_n_delete', args=['100002348657672']))
        self.assertEqual(404, resp.status_code)