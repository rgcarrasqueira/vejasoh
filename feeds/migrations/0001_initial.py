# Generated by Django 2.2.4 on 2019-08-04 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nome da Revista')),
                ('url', models.URLField(verbose_name='Endereço da Revista')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated', models.DateField(auto_now=True, verbose_name='Última atualização em')),
            ],
            options={
                'verbose_name': 'Stream Feed',
                'verbose_name_plural': 'Stream Feeds',
            },
        ),
    ]
