import time
import json

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

from core.models import Drug, Route, MOA


class Command(BaseCommand):
    """Django command to load the database"""

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def build_moa_table(self, data_list):
        self.stdout.write('Building MOA table')
        database_moa = set()
        for data in data_list:
            try:
                for moa in data.get('pharm_class', []):
                    if 'MoA' in moa:
                        database_moa.add(moa[:-6])
            except Exception as err:
                self.stdout.write('Invalid MoA structure:' + str(err))
                continue
        for item in database_moa:
            exists = MOA.objects.filter(moa=item).exists()
            if not exists:
                MOA.objects.create(moa=item)

    def link_drug_moa(self, data_list):
        self.stdout.write("Linking MOA to drug table")
        for data in data_list:
            d = Drug.objects.get(
                product_id=data.get('product_id', ""))
            if d:
                try:
                    for moa in data.get('pharm_class', []):
                        if 'MoA' in moa:
                            m = MOA.objects.get(moa=moa[:-6])
                            d.moa.add(m.id)
                except Exception as err:
                    self.stdout.write("Invalid MOA link:" + str(err))

    def build_routes_table(self, data_list):
        self.stdout.write('Building routes table')
        database_routes = set()
        for data in data_list:
            try:
                for route in data.get('route', []):
                    database_routes.add(route)
            except Exception as err:
                self.stdout.write("Invalid route structure:" + str(err))
                continue
        for item in database_routes:
            exists = Route.objects.filter(route=item).exists()
            if not exists:
                Route.objects.create(route=item)

    def link_drug_routes(self, data_list):
        self.stdout.write('Linking routes to drug table')
        for data in data_list:
            d = Drug.objects.get(
                product_id=data.get('product_id', ""))
            if d:
                try:
                    for route in data.get('route', []):
                        r = Route.objects.get(route=route)
                        d.routes.add(r.id)
                except Exception as err:
                    self.stdout.write("Invalid route link:" + str(err))

    def handle(self, *args, **options):
        self.stdout.write("Loading the database...")
        with open(options['json_file']) as f:
            data_list = json.load(f)

        self.build_routes_table(data_list['results'])
        self.build_moa_table(data_list['results'])

        database_drugs = []
        self.stdout.write("Building drugs table")
        for data in data_list['results']:
            try:
                product_id = data.get('product_id', "").lower()[:254]
                if Drug.objects.filter(product_id=product_id).exists():
                    continue
                generic_name = data.get('generic_name', "").lower()[:254]
                brand_name = data.get('brand_name', "").lower()[:254]
                drug = Drug(product_id=product_id,
                            generic_name=generic_name,
                            brand_name=brand_name)
                if product_id:
                    database_drugs.append(drug)
            except Exception as err:
                self.stdout.write('Invalid drug structure' + str(err))
                continue
        Drug.objects.bulk_create(database_drugs)

        self.link_drug_routes(data_list['results'])
        self.link_drug_moa(data_list['results'])

        self.stdout.write("Database load complete")
