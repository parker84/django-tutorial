# Generated by Django 5.0 on 2023-12-23 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_customer_birth_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='last_update_at',
            new_name='last_update',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='customer',
            name='birth_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(),
        ),
    ]
