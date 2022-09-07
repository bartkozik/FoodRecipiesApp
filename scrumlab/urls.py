"""scrumlab URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko import views

from jedzonko import views
from jedzonko.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('recipe/list/', views.RecipeListLinkView.as_view(), name='przepisy'),
    path('main/', views.DashboardView.as_view(), name='main'),
    path('plan/list/', views.PlanListView.as_view(), name='lista_planow'),
    path('recipe/add/', views.AddRecipeView.as_view(), name='dodanie_nowego_przepisu'),
    path('plan/add/', views.AddPlanView.as_view(), name='dodanie_nowego_planu'),
    path('plan/add-recipe/', views.AddRecipeToPlanView.as_view(), name='dodanie_przepisu_do_planu'),
    path('recipe/<int:id>/', views.RecipeDetailsView.as_view(), name='szczegoly_przepisu'),
    path('recipe/modify/<int:id>/', views.ModifyRecipeView.as_view(), name='modyfikacja_przepisu'),
    path('plan/<int:id>/', views.PlanDetailsView.as_view(), name='szczegoly_planu'),
    path('najlepsze-papu-w-galaktyce/', views.AboutApplicationView.as_view(), name='app_info'),
    path('nasze-dane-kontaktowe/', views.ContactView.as_view(), name='kontakt'),
]
