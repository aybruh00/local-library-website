# Generated by Django 3.2 on 2021-04-21 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
