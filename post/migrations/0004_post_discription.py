# Generated by Django 5.0.4 on 2024-05-02 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='discription',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
