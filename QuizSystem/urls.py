from django.contrib import admin
from django.urls import path
#from LearnAJAX import views as a
from quiz import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.RegisterFormView.as_view()),
    path('login/', views.LoginFormView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view()),
    path('', views.welcome),
    path('quiz/', views.index),
    path('show_answers/', views.show_answers, name="show_answers"),
    path('save_ans/',views.save_ans,name="saveans"),
    path('result/',views.result,name="result"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)