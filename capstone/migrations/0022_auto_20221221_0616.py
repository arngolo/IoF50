# Generated by Django 3.2.16 on 2022-12-20 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0021_auto_20221221_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagery',
            name='spectral_index_color_palette',
            field=models.TextField(db_column='spectral_index_color_palette', default=''),
        ),
        migrations.AddField(
            model_name='imagery',
            name='spectral_index_name',
            field=models.TextField(db_column='spectral_index_name', default=''),
        ),
    ]
