# Generated by Django 3.2.18 on 2023-10-11 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr', '0007_auto_20231011_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='info_text',
            field=models.TextField(default=None, verbose_name='文本'),
        ),
        migrations.AlterField(
            model_name='info',
            name='url',
            field=models.CharField(default=None, max_length=256, verbose_name='url(文本二选一填写)'),
        ),
    ]
