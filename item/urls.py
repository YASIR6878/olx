from django.urls import path
from .import views
app_name='item'
urlpatterns = [
    path('',views.search,name="search"),
    path('sell',views.sell,name="sell"),
    path('<int:pk>/',views.detail,name="detail"),
    path('<int:pk>/delete/',views.delete,name="delete"),
    path('<int:pk>/edit/sell',views.edit,name="edit"),
    


]
