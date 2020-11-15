import requests
from datetime import date, timedelta, datetime

from django.core.management.base import BaseCommand

from core.models import Drug, Route, MOA


class Command(BaseCommand):
    """Django command to load the database"""

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
                pass
        for item in database_routes:
            exists = Route.objects.filter(route=item).exists()
            if not exists:
                Route.objects.create(route=item)

    def link_drug_routes(self, data_list):
        self.stdout.write('Linking routes to drug table')
        for data in data_list:
            d = Drug.objects.get(product_id=data.get('product_id', ""))
            if d:
                try:
                    for route in data.get('route', []):
                        r = Route.objects.get(route=route)
                        d.routes.add(r.id)
                except Exception as err:
                    self.stdout.write("Invalid route link:" + str(err))

    def handle(self, *args, **options):
        self.stdout.write("Loading the database...")
        now = str(date.today().strftime("%Y%m%d"))
        previous = str((date.today() - timedelta(120)).strftime("%Y%m%d"))
        url = f"https://api.fda.gov/drug/ndc.json?search=marketing_start_date:[{previous}+TO+{now}]&limit=100"
        while True:
            r = requests.get(url)
            link = r.links
            if r.status_code != 200:
                quit()
            else:
                data_list = r.json()
        
            self.build_routes_table(data_list['results'])
            self.build_moa_table(data_list['results'])

            database_drugs = []
            self.stdout.write("Building drugs table")
            for data in data_list['results']:
                try:
                    product_id = data.get('product_id', "").lower()[:254]
                    if Drug.objects.filter(product_id=product_id).exists():
                        self.stdout.write("Drug exists: " + product_id)
                        continue
                    product_ndc = data.get('product_ndc', "").lower()[:13]
                    start_date = data.get('marketing_start_date', "").lower()[:8]
                    end_date = data.get('listing_expiration_date', "").lower()[:8]
                    generic_name = data.get('generic_name', "").lower()[:254]
                    brand_name = data.get('brand_name', "").capitalize()[:254]
                    dea_schedule = data.get('dea_schedule', "Legend")
                    drug = Drug(product_id=product_id,
                                product_ndc=product_ndc,
                                start_date=start_date,
                                end_date=end_date,
                                generic_name=generic_name,
                                brand_name=brand_name,
                                dea_schedule=dea_schedule)
                    if product_id:
                        database_drugs.append(drug)
                except Exception as err:
                    self.stdout.write('Invalid drug structure' + str(err))
            Drug.objects.bulk_create(database_drugs)

            self.link_drug_routes(data_list['results'])
            self.link_drug_moa(data_list['results'])

            if link:
                url = link['next']['url']
            else:
                self.stdout.write("Completed entire list")
                break

        self.stdout.write("Database load complete")
