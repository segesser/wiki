from django.urls import path
from . import contact
from . import views

app_name = "wiki"
urlpatterns = [
    path("/", views.index, name="index"),
    path("/new", views.new, name="new"),
    path("/random", views.randomentry, name="random"),
    path("/contact", contact.contact, name='contact'), 
    path("/search", views.search, name="search"),

    path("/edit/<str:entry_name>", views.edit, name="edit"),
    path("/<str:entry_name>", views.entry, name="entry"),
    
]
