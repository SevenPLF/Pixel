# Generated by Django 5.0.2 on 2024-03-12 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixel', '0006_remove_pixel_c_z_alter_pixel_c_del_time2_and_more'),
    ]

    operations = [

        migrations.AlterField(
            model_name='pixel_c',
            name='update_time1',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='pixel_c',
            name='update_time2',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='pixel_c',
            name='update_time3',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
