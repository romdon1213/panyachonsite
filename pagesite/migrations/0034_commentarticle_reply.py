# Generated by Django 3.0.5 on 2020-04-30 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagesite', '0033_remove_post_savelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentarticle',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='pagesite.CommentArticle'),
        ),
    ]