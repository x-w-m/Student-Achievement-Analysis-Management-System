# """
# URL configuration for djangoProject1 project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

from django.urls import path

from cjfx import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('filedown/', views.export_page),
    path('download/', views.export_to_excel, name='download'),
    path('tops/', views.top_students, name='top-students'),
    path('chart/<str:chart_id>/', views.chart_view, name='chart_view')
]
