# Generated by Django 2.1.2 on 2018-10-06 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spcv1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='user',
        ),
    ]
