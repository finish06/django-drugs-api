from django.test import TestCase
from core import models


class ModelTest(TestCase):

    def test_create_drug_successful(self):
        """Test successful creation of a new drug"""
        drug = models.Drug.objects.create(
            generic_name="lisinopril",
            brand_name="Zestril"
        )

        self.assertEqual(str(drug), drug.generic_name)

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
