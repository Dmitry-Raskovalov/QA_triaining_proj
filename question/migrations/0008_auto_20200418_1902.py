# Generated by Django 3.0.5 on 2020-04-18 19:02
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def merge_relations(apps, schema_editor):
    Comment = apps.get_model('question', 'Comment')
    for comment in Comment.objects.all():
        comment.content_object = comment.answer if comment.answer else comment.question
        comment.content_type = ContentType.objects.get_for_model(comment.content_object)
        comment.object_id = comment.content_object.id


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_auto_20200418_1801'),
    ]

    operations = [
        migrations.RunPython(merge_relations)
    ]