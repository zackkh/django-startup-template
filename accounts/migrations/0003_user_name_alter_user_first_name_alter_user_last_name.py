# Generated by Django 4.2.4 on 2023-09-13 18:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_is_deletable_user_is_editable"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.TextField(
                blank=True, editable=False, null=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=150, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=150, verbose_name="last name"),
        ),
    ]
