# Generated by Django 2.2.7 on 2020-01-11 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0003_auto_20200111_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='recipeapp.Tag'),
        ),
    ]
