# Generated by Django 5.0.2 on 2024-03-13 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixel', '0009_remove_pixel_c_z_pixel_c_update_time_and_more'),
    ]

    operations = [

        migrations.AlterField(
            model_name='pixel_c',
            name='z1',
            field=models.CharField(default='4294967295', max_length=22),
        ),
        migrations.AlterField(
            model_name='pixel_c',
            name='z2',
            field=models.CharField(default='4294967295', max_length=22),
        ),
        migrations.AlterField(
            model_name='pixel_c',
            name='z3',
            field=models.CharField(default='4294967295', max_length=22),
        ),
    ]
