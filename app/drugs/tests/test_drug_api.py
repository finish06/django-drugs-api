from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Drug

from drugs.serializers import DrugSerializer

DRUGS_URL = reverse('drugs:drug-list')


def sample_drug(**params):
    """Create a sample drug to load into the DB"""
    defaults = {
        'generic_name': 'lisinopril',
        'brand_name': 'zestril'
    }
    defaults.update(params)

    return Drug.objects.create(**defaults)

class PublicDrugsApiTest(TestCase):
    """Test unauthenticated drugs API access"""

    def setUp(self):
        self.client = APIClient()

    def test_create_drug(self):
        """Test the ability to save a drug to the DB"""
        payload = {
        'generic_name': 'lisinopril',
        'brand_name': 'zestril',
        'product_id': '123456'
        }
        Drug.objects.create(**payload)

        exists = Drug.objects.exists()

        self.assertTrue(exists)

    def test_retrieve_drugs(self):
        """Test retrieving a drug from the db"""
        sample_drug()
        
        res = self.client.get(DRUGS_URL)
        drug = Drug.objects.all()
        serializer = DrugSerializer(drug, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_drug_filter_generic(self):
        """Test the ability to filter to select generics"""
        drug1 = sample_drug()
        drug2 = sample_drug(
            generic_name='metoprolol',
            brand_name='lopressor',
            product_id="345678"
        )

        res = self.client.get(DRUGS_URL, {'generic': 'lisinopril'})

        serializer1 = DrugSerializer(drug1)
        serializer2 = DrugSerializer(drug2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2, res.data)

    def test_retrieve_drug_filter_brand(self):
        """Test the ability to filter to select brands"""
        drug1 = sample_drug()
        drug2 = sample_drug(
            generic_name='metoprolol',
            brand_name='lopressor'
        )

        res = self.client.get(DRUGS_URL, {'brand': 'lopressor'})

        serializer1 = DrugSerializer(drug1)
        serializer2 = DrugSerializer(drug2)

        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer1, res.data)

    def test_retrieve_drug_filter_product_id(self):
        """Test the ability to filter to product ID"""
        drug1 = sample_drug()
        drug2 = sample_drug(
            generic_name='metoprolol',
            brand_name='lopressor',
            product_id="345678"
        )

        res = self.client.get(DRUGS_URL, {'product_id': '345678'})

        serializer1 = DrugSerializer(drug1)
        serializer2 = DrugSerializer(drug2)

        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer1, res.data)
