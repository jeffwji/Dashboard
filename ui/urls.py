from django.urls import path
from ui import views

"""
URL definition
"""
urlpatterns = [
    # Default page
    path('', views.index, name='index'),
    path('contribute', views.contribute, name='contribute'),
]
