from django.urls import path
from . import views

# path('RiskTree/', include('RiskTree.urls')),
urlpatterns = [
    path('CorrelatedHistogram/', views.CorrelatedHistogram),
    path('GetAttrCorrelation/', views.GetAttrCorrelation),
]
