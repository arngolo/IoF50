# Generated by Django 3.2.16 on 2022-11-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0016_imagery_kmeans'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagery',
            name='band_stack_list',
            field=models.TextField(db_column='band_stack_list', default='', max_length=300),
        ),
    ]
