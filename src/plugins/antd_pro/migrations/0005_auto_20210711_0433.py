# Generated by Django 3.2.4 on 2021-07-11 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antd_pro', '0004_antdcasbinrule_antdmenurule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='antdrole',
            name='permissions',
        ),
        migrations.AlterField(
            model_name='antdrole',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antd_pro.antdrole', verbose_name='上级角色'),
        ),
    ]
