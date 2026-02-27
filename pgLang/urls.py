from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),   
    path('exemplu/', views.afis_template, name='exemplu'),
    path('info/', views.info, name='info'),
    path('artisti/', views.lista_artisti, name='lista-artisti'),    
    path('artisti/<int:artist_id>/', views.detaliu_artist, name='detaliu-artist'),
    path('artisti/adauga/', views.adauga_artist, name='adauga-artist'),
    path('gen/<slug:gen_slug>/', views.detaliu_gen, name='detaliu-gen'),
    path('contact/', views.pagina_contact, name='contact'),
    path('album/<int:album_id>/', views.detaliu_album, name='detaliu-album'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profil/', views.profil, name='profil'),
    path('schimbare-parola/', views.schimbare_parola, name='schimbare-parola'),
    path('confirma_mail/<str:cod>/', views.confirma_mail, name='confirma-mail'),
]