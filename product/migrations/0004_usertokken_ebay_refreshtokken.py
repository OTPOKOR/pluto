# Generated by Django 4.0.3 on 2022-03-08 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_description_bottom_remove_ebay_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertokken',
            name='ebay_refreshtokken',
            field=models.TextField(null=True),
        ),
    ]
