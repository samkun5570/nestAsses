# Generated by Django 3.1.2 on 2020-10-23 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employeeId',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
