from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ('carros', '0010_add_modelo_versao'),
]


    operations = [
        migrations.AddField(
            model_name='carro',
            name='categoria',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='carros.CategoriaVeiculo'),
        ),

        migrations.AddField(
            model_name='carro',
            name='modelo',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='carros.ModeloVeiculo'),
        ),

        migrations.AddField(
            model_name='carro',
            name='versao',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='carros.VersaoVeiculo'),
        ),

        migrations.AddField(
            model_name='carro',
            name='km',
            field=models.PositiveIntegerField(default=0),
        ),

        migrations.AddField(
            model_name='carro',
            name='cor',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),

        migrations.AddField(
            model_name='carro',
            name='portas',
            field=models.PositiveSmallIntegerField(default=4),
        ),

        migrations.AddField(
            model_name='carro',
            name='combustivel',
            field=models.CharField(
                max_length=20,
                choices=[
                    ("gasolina", "Gasolina"),
                    ("etanol", "Etanol"),
                    ("flex", "Flex"),
                    ("diesel", "Diesel"),
                    ("eletrico", "Elétrico"),
                    ("hibrido", "Híbrido"),
                ],
                default="flex"
            ),
        ),

        migrations.AddField(
            model_name='carro',
            name='cambio',
            field=models.CharField(
                max_length=20,
                choices=[
                    ("manual", "Manual"),
                    ("automatico", "Automático"),
                    ("cvt", "CVT"),
                    ("automatizado", "Automatizado"),
                ],
                default="manual"
            ),
        ),

        migrations.AddField(
            model_name='carro',
            name='destacado',
            field=models.BooleanField(default=False),
        ),
    ]
