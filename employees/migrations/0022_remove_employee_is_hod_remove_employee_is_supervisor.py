# Generated by Django 4.0.3 on 2022-03-16 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0021_alter_department_hod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='is_hod',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='is_supervisor',
        ),
    ]
