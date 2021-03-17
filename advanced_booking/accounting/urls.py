from django.urls import path

from . import views

urlpatterns = [
    path('accounting', views.accounting, name='accounting'),
    path('accounting/movie/<int:movie_id>/', views.movie_income, name='movie income'),
    path('accounting/compare', views.compare, name='compare'),
]
