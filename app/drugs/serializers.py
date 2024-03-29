from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin

from core.models import Generic, Drug, Route, MOA


class GenericSerializer(serializers.ModelSerializer):

    class Meta:
        model = Generic
        fields = ('id', 'generic_name')
        read_only_fields = ('id',)


class MOASerializer(serializers.ModelSerializer):

    class Meta:
        model = MOA
        fields = ('id', 'moa')
        ready_only_fields = ('id',)


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ('id', 'route')
        ready_only_fields = ('id',)


class DrugSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """Serializer for drug object"""

    # moa = MOASerializer(many=True, read_only=True)
    # routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = Drug
        fields = ('id', 'product_id', 'product_ndc', 'start_date',
                  'end_date', 'generic_name', 'brand_name',
                  'routes', 'moa', 'dea_schedule')
        ready_only_fields = ('id',)
