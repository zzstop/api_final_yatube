# Generated by Django 3.1.7 on 2021-03-02 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_post_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
    ]
