# Generated by Django 3.2 on 2021-05-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0007_userstatus_typing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='owner',
            field=models.CharField(max_length=50),
        ),
    ]
