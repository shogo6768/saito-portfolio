# Generated by Django 3.1.4 on 2020-12-02 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ITsupermanapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postmodel',
            old_name='categorys',
            new_name='category',
        ),
    ]