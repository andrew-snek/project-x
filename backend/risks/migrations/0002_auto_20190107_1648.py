# Generated by Django 2.1.5 on 2019-01-07 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AbstractRisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('field_types', models.ManyToManyField(related_name='abstract_risks', through='risks.AbstractField', to='risks.FieldType')),
            ],
        ),
        migrations.AddField(
            model_name='abstractfield',
            name='abstract_risk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abstract_fields', to='risks.AbstractRisk'),
        ),
        migrations.AddField(
            model_name='abstractfield',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='risks.FieldType'),
        ),
    ]
