# Generated by Django 3.0.3 on 2020-03-28 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coronamap', '0005_covid19infobycountry_difference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covid19infobycountry',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
