# Generated by Django 3.2.16 on 2022-11-16 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0014_imagery_pqkmeans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagery',
            name='normalized_difference',
        ),
        migrations.AddField(
            model_name='imagery',
            name='spectral_index_equation',
            field=models.TextField(db_column='spectral_index_equation', default=''),
        ),
        migrations.AddField(
            model_name='imagery',
            name='spectral_index_name',
            field=models.TextField(db_column='spectral_index_name', default=''),
        ),
    ]
