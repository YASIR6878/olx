from django.urls import path

from .import views
app_name='conversation'
urlpatterns = [
    path('',views.inbox,name="inbox"),
    path('chat/<int:item_pk>/',views.contact,name='contact'),
    path('<int:pk>/',views.inboxdetail,name='inboxdetail'),
]
