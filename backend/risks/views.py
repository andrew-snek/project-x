from django.db import transaction
from django.db.models.deletion import ProtectedError
from rest_framework.generics import DestroyAPIView,  ListCreateAPIView
from risks.models import FieldType, AbstractRisk, Risk
from risks.serializers import (
    FieldTypeSerializer, AbstractRiskSerializer, RiskSerializer
)
from risks.exceptions import CannotDeleteAlreadyInUse


class FieldTypeList(DestroyAPIView, ListCreateAPIView):
    serializer_class = FieldTypeSerializer

    def get_queryset(self):
        return FieldType.objects.all()

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except ProtectedError:
            raise CannotDeleteAlreadyInUse


class AbstractRiskList(DestroyAPIView, ListCreateAPIView):
    serializer_class = AbstractRiskSerializer

    def get_queryset(self):
        return AbstractRisk.objects.all()

    def perform_destroy(self, instance):
        with transaction.atomic():
            try:
                super().perform_destroy(instance)
            except ProtectedError:
                raise CannotDeleteAlreadyInUse


class RiskList(DestroyAPIView, ListCreateAPIView):
    serializer_class = RiskSerializer

    def get_queryset(self):
        return Risk.objects.all()

    def perform_destroy(self, instance):
        with transaction.atomic():
            super().perform_destroy(instance)
