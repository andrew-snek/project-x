from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from risks.views import FieldTypeList, AbstractRiskList, RiskList

urlpatterns = [
    path('obtain-token/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('api/v1/fieldtypes/', FieldTypeList.as_view()),
    path('api/v1/fieldtypes/<int:pk>', FieldTypeList.as_view()),
    path('api/v1/abstractrisks/', AbstractRiskList.as_view()),
    path('api/v1/abstractrisks/<int:pk>', AbstractRiskList.as_view()),
    path('api/v1/risks/', RiskList.as_view()),
    path('api/v1/risks/<int:pk>', RiskList.as_view())
]
