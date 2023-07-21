"""
URL configuration for QuizProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from .views import (
    QuizListCreateView,UserQuizTakingView,UserQuizScoreView,QuizListView,
    QuizAnalyticsView
)


urlpatterns = [
    path('create/',QuizListCreateView.as_view(),name='create-quiz'),
    path('list/filter/',QuizListView.as_view(),name='filterlist-quiz'),
    path('take/<int:pk>/',UserQuizTakingView.as_view(),name='take-quiz'),
    path('score/',UserQuizScoreView.as_view(),name='quiz-score'),
    path('analytics/',QuizAnalyticsView.as_view(),name='quiz-analytics')

]
