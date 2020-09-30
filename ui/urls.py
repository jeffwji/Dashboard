from django.urls import path
from ui import views

"""
URL definition
"""
urlpatterns = [
    # Default page
    path('', views.hello_world, name='hello_world'),
]
