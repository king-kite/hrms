# Generated by Django 4.0.3 on 2022-03-24 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0023_alter_employee_date_employed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='status',
        ),
    ]
