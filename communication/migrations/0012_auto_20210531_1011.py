# Generated by Django 3.2 on 2021-05-31 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0011_alter_groups_groupid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Groups',
        ),
        migrations.AlterField(
            model_name='messages',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
