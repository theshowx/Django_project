# Generated by Django 2.0.5 on 2018-06-01 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_komentarz_odpowiedz_artykul'),
    ]

    operations = [
        migrations.AddField(
            model_name='komentarz_odpowiedz',
            name='dataZamieszczenia',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data zamieszczenia'),
        ),
    ]
