import json
from datetime import datetime

from django.core.management.base import BaseCommand

from core.models import Generic, Drug, Route, MOA


class Command(BaseCommand):
    """Django command to load the database"""

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def build_moa_table(self, data_list):
        self.stdout.write(f'{str(datetime.now())} -- Building MOA table')
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
        self.stdout.write(f'{str(datetime.now())} -- '
                          'Linking MOA to drug table')
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
        self.stdout.write(f'{str(datetime.now())} -- Building routes table')
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
        self.stdout.write(f'{str(datetime.now())} -- '
                          'Linking routes to drug table')
        for data in data_list:
            try:
                d = Drug.objects.get(
                    product_id=data.get('product_id', ""))
            except Exception as err:
                self.stdout.write(f"{str(datetime.now())} -- ' \
                                    'Product ID does not exist: {err}")
                continue
            if d:
                try:
                    for route in data.get('route', []):
                        r = Route.objects.get(route=route)
                        d.routes.add(r.id)
                except Exception as err:
                    self.stdout.write("Invalid Route link:" + str(err))

    def build_generics_table(self, data_list):
        self.stdout.write(f'{str(datetime.now())} -- Building generics table')
        database_generics = set()
        for data in data_list:
            try:
                generic_name = data.get('generic_name', "")
                database_generics.add(generic_name.lower()[:254])
            except Exception as err:
                self.stdout.write(f'{str(datetime.now())} -- '
                                  f'Generic name does not exist: {err}')
                continue
        objs = [
            Generic(
                generic_name=item
            )
            for item in database_generics
        ]
        Generic.objects.bulk_create(objs=objs)
        # for item in database_generics:
        #     exists = Generic.objects.filter(generic_name=item).exists()
        #     if not exists:
        #         Generic.objects.create(generic_name=item)

    def handle(self, *args, **options):
        self.stdout.write("Loading the database...")
        with open(options['json_file']) as f:
            data_list = json.load(f)

        self.build_routes_table(data_list['results'])
        self.build_moa_table(data_list['results'])
        self.build_generics_table(data_list['results'])

        database_drugs = []
        new_data = []
        self.stdout.write(f'{str(datetime.now())} -- Building drugs table')
        for data in data_list['results']:
            try:
                product_id = data.get('product_id', "").lower()[:254]
                product_ndc = data.get('product_ndc', "").lower()[:13]
                start_date = data.get('marketing_start_date', "").lower()[:8]
                end_date = data.get('listing_expiration_date', "").lower()[:8]
                generic_name = data.get('generic_name', "")
                generic_obj = Generic.objects.get(
                        generic_name=generic_name.lower()[:254])
                brand_name = data.get('brand_name', "").capitalize()[:254]
                dea_schedule = data.get('dea_schedule', "Legend")
                drug = Drug(product_id=product_id,
                            product_ndc=product_ndc,
                            start_date=start_date,
                            end_date=end_date,
                            generic_name=generic_obj,
                            brand_name=brand_name,
                            dea_schedule=dea_schedule)
                database_drugs.append(drug)
                new_data.append(data)
            except Exception as err:
                self.stdout.write('Invalid drug structure -- ' + str(err))
                continue
        self.stdout.write(f'{str(datetime.now())} -- '
                          'Bulk inserting drugs table')
        Drug.objects.bulk_create(database_drugs)

        self.link_drug_routes(new_data)
        self.link_drug_moa(new_data)

        self.stdout.write(f'{str(datetime.now())} -- Database load complete')
