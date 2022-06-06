# Generated by Django 4.0.3 on 2022-06-05 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_remove_projectfile_image_projectfile_file_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.employee'),
        ),
    ]