# Generated by Django 5.0.2 on 2024-04-03 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixel', '0014_pixel_a_pixel_b_remove_pixel_c_z_lable_z'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Pixel_A',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('x', models.IntegerField()),
        #         ('y', models.IntegerField()),
        #         ('z1', models.CharField(default='4294967295', max_length=22)),
        #         ('z2', models.CharField(default='4294967295', max_length=22)),
        #         ('z3', models.CharField(default='4294967295', max_length=22)),
        #         ('lable1', models.CharField(default='', max_length=255)),
        #         ('lable2', models.CharField(default='', max_length=255)),
        #         ('lable3', models.CharField(default='', max_length=255)),
        #         ('update_time1', models.DateTimeField(auto_now_add=True)),
        #         ('update_time2', models.DateTimeField(auto_now_add=True)),
        #         ('update_time3', models.DateTimeField(auto_now_add=True)),
        #         ('del_time1', models.BigIntegerField(default=300)),
        #         ('del_time2', models.BigIntegerField(default=300)),
        #         ('del_time3', models.BigIntegerField(default=300)),
        #         ('update_time', models.DateTimeField(auto_now=True)),
        #     ],
        # ),
        # migrations.CreateModel(
        #     name='Pixel_B',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('x', models.IntegerField()),
        #         ('y', models.IntegerField()),
        #         ('z1', models.CharField(default='4294967295', max_length=22)),
        #         ('z2', models.CharField(default='4294967295', max_length=22)),
        #         ('z3', models.CharField(default='4294967295', max_length=22)),
        #         ('lable1', models.CharField(default='', max_length=255)),
        #         ('lable2', models.CharField(default='', max_length=255)),
        #         ('lable3', models.CharField(default='', max_length=255)),
        #         ('update_time1', models.DateTimeField(auto_now_add=True)),
        #         ('update_time2', models.DateTimeField(auto_now_add=True)),
        #         ('update_time3', models.DateTimeField(auto_now_add=True)),
        #         ('del_time1', models.BigIntegerField(default=300)),
        #         ('del_time2', models.BigIntegerField(default=300)),
        #         ('del_time3', models.BigIntegerField(default=300)),
        #         ('update_time', models.DateTimeField(auto_now=True)),
        #     ],
        # ),
        # migrations.RemoveField(
        #     model_name='pixel_c',
        #     name='z',
        # ),
        migrations.AddField(
            model_name='lable',
            name='index_abc',
            field=models.CharField(default=1, max_length=22),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lable',
            name='pixel_id',
            field=models.IntegerField(),
        ),
    ]
