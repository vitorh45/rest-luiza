__author__ = 'vitor'

from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'core.views.person', name='person'),
]