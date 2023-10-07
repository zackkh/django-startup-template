# Generated by Django 4.2.4 on 2023-09-13 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "accounts",
            "0003_user_name_alter_user_first_name_alter_user_last_name",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_deletable",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_editable",
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.TextField(
                blank=True, default="", editable=False, verbose_name="name"
            ),
            preserve_default=False,
        ),
    ]
