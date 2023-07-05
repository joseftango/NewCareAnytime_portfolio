from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', views.home, name="home"),
    path('caretaker_register', views.caretaker_register, name="caretaker_register"),
    path('careseeker_register', views.careseeker_register, name="careseeker_register"),
    path('login', views.login_view, name="login_view"),
    path('all_members', views.all_members, name="all_members"),
    path('logout', views.logout_view, name="logout_view"),
    path('user_profile', views.user_profile, name='user_profile'),
    path('about_us', views.about_us, name="about_us"),
    path('services', views.services, name="services"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

