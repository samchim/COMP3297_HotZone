# Generated by Django 3.1.2 on 2020-10-31 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caseNumber', models.CharField(max_length=200)),
                ('dateConfirmed', models.DateField()),
                ('localOrImported', models.CharField(max_length=200)),
                ('patientName', models.CharField(max_length=200)),
                ('idNumber', models.CharField(max_length=200)),
                ('dateOfBirth', models.DateField()),
                ('virusName', models.CharField(max_length=200)),
                ('disease', models.CharField(max_length=200)),
                ('maxInfectiousPeriod', models.DecimalField(decimal_places=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='LocationCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locationName', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('xCord', models.DecimalField(decimal_places=0, max_digits=6)),
                ('yCord', models.DecimalField(decimal_places=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateFrom', models.DateField()),
                ('dateTo', models.DateField()),
                ('category', models.CharField(max_length=200)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recordPage.case')),
                ('locationCache', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recordPage.locationcache')),
            ],
        ),
    ]