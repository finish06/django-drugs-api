# Generated by Django 3.0.8 on 2020-07-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_drug_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='product_id',
            field=models.CharField(max_length=255),
        ),
    ]
