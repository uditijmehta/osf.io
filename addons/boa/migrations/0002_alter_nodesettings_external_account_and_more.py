# Generated by Django 4.2.13 on 2024-07-15 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0021_preprint_custom_publication_citation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addons_boa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodesettings',
            name='external_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_node_settings', to='osf.externalaccount'),
        ),
        migrations.AlterField(
            model_name='nodesettings',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_node_settings', to='osf.abstractnode'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_user_settings', to=settings.AUTH_USER_MODEL),
        ),
    ]
