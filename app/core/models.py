from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
#                                        PermissionsMixin


class Generic(models.Model):
    """List of generic medication names"""
    generic_name = models.CharField(max_length=255)

    def __str__(self):
        return self.generic_name


class Drug(models.Model):
    """Drug database from OpenFDA data"""
    product_id = models.CharField(max_length=255)
    product_ndc = models.CharField(max_length=13)
    start_date = models.CharField(max_length=8)
    end_date = models.CharField(max_length=8)
    generic_name = models.ForeignKey('Generic', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255)
    dea_schedule = models.CharField(max_length=10, null=True)
    routes = models.ManyToManyField('Route')
    moa = models.ManyToManyField('MOA')

    def __str__(self):
        return self.product_id + " " + self.product_ndc


class Route(models.Model):
    """Routes database from OpenFDA data"""
    route = models.CharField(max_length=255)

    def __str__(self):
        return self.route


class MOA(models.Model):
    """MOA databsae from OpenFDA data"""
    moa = models.CharField(max_length=255)

    def __str__(self):
        return self.moa
