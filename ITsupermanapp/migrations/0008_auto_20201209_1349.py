# Generated by Django 3.1.4 on 2020-12-09 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ITsupermanapp', '0007_auto_20201209_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='ITsupermanapp.parentcategory'),
        ),
    ]