from rest_framework import serializers

from core.models import Drug, Route, MOA


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


class DrugSerializer(serializers.ModelSerializer):
    """Serializer for drug object"""

    moa = MOASerializer(many=True, read_only=True)
    routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = Drug
        fields = ('id', 'product_id', 'generic_name', 'brand_name', 'routes', 'moa', 'dea_schedule')
        ready_only_fields = ('id',)
