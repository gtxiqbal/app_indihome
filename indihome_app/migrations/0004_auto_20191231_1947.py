# Generated by Django 3.0.1 on 2019-12-31 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indihome_app', '0003_auto_20191231_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gpon',
            options={'ordering': ['hostname'], 'verbose_name': 'Gpon', 'verbose_name_plural': 'Gpon'},
        ),
    ]