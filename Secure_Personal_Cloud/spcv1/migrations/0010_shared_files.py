# Generated by Django 2.1.2 on 2018-11-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spcv1', '0009_encryption'),
    ]

    operations = [
        migrations.CreateModel(
            name='shared_files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=100)),
                ('reciever', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
            ],
        ),
    ]
