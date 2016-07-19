from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^processSearchTerm$', views.process_search_term, name='process_search_term'),
    url(r'^checkIndex$', views.check_index, name='check_index'),
]
