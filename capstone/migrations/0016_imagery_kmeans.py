# Generated by Django 3.2.16 on 2022-11-23 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0015_auto_20221117_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagery',
            name='kmeans',
            field=models.TextField(db_column='kmeans', default='kmeans'),
        ),
    ]
