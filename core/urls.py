__author__ = 'vitor'

from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<fbid>[\w_-]+)/$', 'core.views.person_detail_n_delete', name='person_detail_n_delete'),
    url(r'^$', 'core.views.person_add_n_list', name='person_add_n_list'),
]