# Generated by Django 3.0.5 on 2020-06-09 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0009_auto_20200418_2017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-action_time'], 'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='url',
        ),
    ]
