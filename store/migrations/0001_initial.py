# Generated by Django 4.2.16 on 2024-09-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantite_en_stock', models.IntegerField()),
                ('image', models.ImageField(upload_to='produits/')),
                ('categorie', models.CharField(choices=[('homme', 'Homme'), ('femme', 'Femme'), ('enfant', 'Enfant')], default='homme', max_length=20)),
            ],
        ),
    ]
