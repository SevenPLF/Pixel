# Generated by Django 5.0.2 on 2024-03-12 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixel', '0007_remove_pixel_c_z_alter_pixel_c_update_time1_and_more'),
    ]

    operations = [

        migrations.AlterField(
            model_name='pixel_c',
            name='lable1',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='pixel_c',
            name='lable2',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='pixel_c',
            name='lable3',
            field=models.CharField(default='', max_length=255),
        ),
    ]
