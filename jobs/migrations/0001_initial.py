# Generated by Django 4.0.3 on 2022-05-29 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('auto_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(editable=False, max_length=7, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
