from django.urls import path
from . import views

# path('RiskTree/', include('RiskTree.urls')),
urlpatterns = [
    path('RLRecommend/', views.RL_recommend),
    path('StrategyRecommend/', views.Strategy_recommend),
]
