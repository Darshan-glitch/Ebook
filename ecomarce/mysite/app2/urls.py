from os import name, stat
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from mysite.settings import MEDIA_ROOT,MEDIA_URL
urlpatterns = [
   

  path("",views.home,name="home"),
  path("login/",views.login,name="login"),
  path("login",views.login,name="login"),
  path("logout",views.logout,name="logout"),
  path('signup',views.register,name="register"),
  path("register",views.register,name="register"),
  path("about",views.about,name="about"),
  path('upload/',views.upload_video,name='upload'),
  path('videos/',views.display,name='videos'),
  path("book",views.book,name="book"),
  path("payment/<int:book_id>",views.payment,name="payment"),
  path("payment/verify",views.verifypayment,name="verifypayment"),
  path("order",views.order,name="order"),
  path("see/<int:book_id>/",views.see,name="see")


] + static(MEDIA_URL,document_root = MEDIA_ROOT)

