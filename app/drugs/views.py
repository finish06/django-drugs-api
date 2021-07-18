from rest_framework import viewsets

from drugs import serializers

from core.models import Generic, Drug, Route, MOA


class GenericViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Generic.objects.all()
    serializer_class = (serializers.GenericSerializer)

    def get_queryset(self):
        queryset = self.queryset
        generic = self.request.query_params.get('generic')
        if generic:
            queryset = Generic.objects.filter(generic=generic)
        return queryset


class RouteViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Route.objects.all()
    serializer_class = (serializers.RouteSerializer)

    def get_queryset(self):
        queryset = self.queryset
        route = self.request.query_params.get('route')
        if route:
            queryset = Route.objects.filter(route=route)
        return queryset


class MoaViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = MOA.objects.all()
    serializer_class = (serializers.MOASerializer)

    def get_queryset(self):
        queryset = self.queryset
        moa = self.request.query_params.get('moa')
        if moa:
            queryset = MOA.objects.filter(moa=moa)
        return queryset


class DrugViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Drug.objects.all()
    serializer_class = (serializers.DrugSerializer)

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        generic_name = self.request.query_params.get('generic')
        brand_name = self.request.query_params.get('brand')
        route = self.request.query_params.get('route')
        moa = self.request.query_params.get('moa')
        schedule = self.request.query_params.get('schedule')
        params = {}
        if schedule:
            params['dea_schedule'] = schedule
        if moa:
            params['moa__moa__iexact'] = moa
        if route:
            params['routes__route__iexact'] = route
        if product_id:
            params['product_id'] = product_id
        if generic_name:
            params['generic_name__generic_name__iexact'] = generic_name
        if brand_name:
            params['brand_name'] = brand_name
        return self.queryset.filter(**params)
        # .distinct('generic_name', 'brand_name')
