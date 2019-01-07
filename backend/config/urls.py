from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from risks.views import FieldTypeList

urlpatterns = [
    path('obtain-token/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('api/v1/fieldtypes/', FieldTypeList.as_view()),
    path('api/v1/fieldtypes/<int:pk>', FieldTypeList.as_view()),
]
