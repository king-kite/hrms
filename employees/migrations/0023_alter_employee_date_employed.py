# Generated by Django 4.0.3 on 2022-03-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0022_remove_employee_is_hod_remove_employee_is_supervisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_employed',
            field=models.DateField(auto_now=True),
        ),
    ]
