# Generated by Django 3.0.5 on 2020-04-15 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagesite', '0009_auto_20200416_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.DeleteModel(
            name='CategoryPost',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]