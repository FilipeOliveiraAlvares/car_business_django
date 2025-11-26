from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ('carros', '0008_favorito'),
]


    operations = [
        migrations.CreateModel(
            name='CategoriaVeiculo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
