# Generated by Django 3.2.16 on 2022-11-15 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0013_auto_20221116_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagery',
            name='pqkmeans',
            field=models.TextField(db_column='pqkmeans', default='pqkmeans'),
        ),
    ]
