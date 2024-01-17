# urls.py

from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('conversation/',include('conversation.urls')),
    path('', views.index, name="index"),
    path('loginuser',views.loginuser,name="loginuser"),
    path('signup',views.signup,name="signup"),
    path('logoutuser',views.logoutuser,name="logoutuser"),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('contact_us',views.contact_us,name="contact_us"),
    path('filterbystates',views.filterbystates,name="filterbystates"),
    path('dashboard/filterbystates',views.filterbystates,name="filterbystates"),
    path('items/',include('item.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('auctions/', include('auctions.urls'))

    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
