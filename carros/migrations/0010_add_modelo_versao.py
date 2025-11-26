from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ('carros', '0009_add_categoria_veiculo'),
]


    operations = [

        migrations.CreateModel(
            name='ModeloVeiculo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carros.Marca')),
            ],
        ),

        migrations.CreateModel(
            name='VersaoVeiculo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carros.ModeloVeiculo')),
            ],
        ),

        migrations.AlterUniqueTogether(
            name='modeloveiculo',
            unique_together={('marca', 'nome')},
        ),
    ]
