# Generated by Django 3.0.4 on 2020-08-30 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DbEntry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationmodel',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
