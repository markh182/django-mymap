# Generated by Django 3.0.3 on 2020-03-24 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coronamap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Covid19Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=30)),
                ('date', models.DateField(null=True)),
                ('confirmed', models.PositiveIntegerField(default=0)),
                ('deaths', models.PositiveIntegerField(default=0)),
                ('recovered', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
