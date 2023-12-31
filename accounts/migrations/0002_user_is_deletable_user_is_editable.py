# Generated by Django 4.2.4 on 2023-09-11 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_deletable",
            field=models.BooleanField(default=True, verbose_name="deletable"),
        ),
        migrations.AddField(
            model_name="user",
            name="is_editable",
            field=models.BooleanField(default=True, verbose_name="editable"),
        ),
    ]
