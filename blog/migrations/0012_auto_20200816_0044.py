# Generated by Django 3.1rc1 on 2020-08-15 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200816_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='usr.png', upload_to='images'),
        ),
    ]