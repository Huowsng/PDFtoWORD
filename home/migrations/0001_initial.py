# Generated by Django 4.2.4 on 2023-08-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConvertedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='pdf_files/')),
                ('docx_file', models.FileField(upload_to='docx_files/')),
                ('converted_at', models.DateTimeField(auto_now_add=True)),
                ('short_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
            ],
        ),
    ]
