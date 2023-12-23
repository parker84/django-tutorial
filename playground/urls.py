from django.urls import path
from . import views
# map urls to view functions

# URL configuration
urlpatterns = [
    path(route='hello/', view=views.say_hello) # always end routes with a /
]


