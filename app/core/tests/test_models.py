from django.test import TestCase
from core import models


class ModelTest(TestCase):

    def test_create_drug_successful(self):
        """Test successful creation of a new drug"""
        generic = models.Generic.objects.create(
            generic_name="Lisinopril"
        )
        print(type(generic))
        drug = models.Drug.objects.create(
            product_id='12345',
            generic_name=generic,
            product_ndc="99999-9999",
            brand_name="Zestril"
        )

        self.assertEqual(str(drug), f"{drug.product_id} {drug.product_ndc}")

    def test_create_route_successful(self):
        """Test successful creation of a new route"""
        route = models.Route.objects.create(
            route="oral"
        )

        self.assertEqual(str(route), route.route)

    def test_create_moa_successful(self):
        """Test successful creation of a new MOA"""
        MOA = models.MOA.objects.create(
            moa="H2 inhibitor"
        )

        self.assertEqual(str(MOA), MOA.moa)
