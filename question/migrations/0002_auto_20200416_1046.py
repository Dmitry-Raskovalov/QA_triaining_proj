# Generated by Django 3.0.5 on 2020-04-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='info',
            field=models.TextField(null=True, verbose_name='Информация'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Имя Фамилия'),
        ),
        migrations.AlterField(
            model_name='author',
            name='nickname',
            field=models.CharField(max_length=100, verbose_name='Отображаемое имя'),
        ),
    ]
