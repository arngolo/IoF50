# Generated by Django 4.0.6 on 2022-08-18 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imagery',
            fields=[
                ('image_id', models.AutoField(db_column='image_id', primary_key=True, serialize=False)),
                ('image_name', models.CharField(blank=True, max_length=200, null=True)),
                ('remote_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('local_image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('image_details', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]
