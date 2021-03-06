# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCommonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(choices=[(b'server', '\u670d\u52a1\u5668'), (b'switch', '\u4ea4\u6362\u673a'), (b'router', '\u8def\u7531\u5668'), (b'firewall', '\u9632\u706b\u5899'), (b'wireless', '\u65e0\u7ebf\u8bbe\u5907'), (b'storage', '\u5b58\u50a8\u8bbe\u5907'), (b'software', '\u8f6f\u4ef6\u8d44\u4ea7'), (b'other', '\u5176\u5b83\u8d44\u4ea7')], default=b'server', max_length=64)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u578b\u53f7')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='\u8d44\u4ea7SN\u53f7')),
                ('management_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='\u7ba1\u7406IP')),
                ('purchase_date', models.DateField(blank=True, null=True, verbose_name='\u8d2d\u4e70\u65f6\u95f4')),
                ('expired_date', models.DateField(blank=True, null=True, verbose_name='\u8fc7\u4fdd\u65f6\u95f4')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='\u8d2d\u4e70\u4ef7\u683c')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u901a\u7528\u4fe1\u606f',
                'verbose_name_plural': '\u8d44\u4ea7\u901a\u7528\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='AssetTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='\u8d44\u4ea7\u6807\u7b7e\u540d\u79f0')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u6807\u7b7e',
                'verbose_name_plural': '\u8d44\u4ea7\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='\u4e1a\u52a1\u7ebf')),
                ('memo', models.TextField(blank=True, verbose_name='\u5907\u6ce8')),
                ('parent_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_level', to='assets.BusinessUnit')),
            ],
            options={
                'verbose_name': '\u4e1a\u52a1\u7ebf',
                'verbose_name_plural': '\u4e1a\u52a1\u7ebf',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u540d\u79f0')),
                ('model', models.CharField(blank=True, max_length=128, verbose_name='\u578b\u53f7')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN\u53f7')),
                ('slot', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u63d2\u69fd\u53f7')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u7ec4\u4ef6\u7684\u901a\u7528\u4fe1\u606f',
                'verbose_name_plural': '\u7ec4\u4ef6\u7684\u901a\u7528\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_no', models.CharField(max_length=128, unique=True, verbose_name='\u5408\u540c\u53f7')),
                ('name', models.CharField(max_length=128, verbose_name='\u5408\u540c\u540d\u79f0')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u5907\u6ce8')),
                ('price', models.IntegerField(verbose_name='\u5408\u540c\u91d1\u989d')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='\u5408\u540c\u8be6\u7ec6')),
                ('start_date', models.DateField(blank=True, verbose_name='\u5408\u540c\u5f00\u59cb\u65f6\u95f4')),
                ('end_date', models.DateField(blank=True, verbose_name='\u5408\u540c\u7ed3\u675f\u65f6\u95f4')),
                ('license_num', models.IntegerField(blank=True, verbose_name='license\u6570\u91cf')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u5408\u540c',
                'verbose_name_plural': '\u5408\u540c',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u4e8b\u4ef6\u540d\u79f0')),
                ('event_type', models.SmallIntegerField(choices=[(1, '\u786c\u4ef6\u53d8\u66f4'), (2, '\u65b0\u589e\u914d\u4ef6'), (3, '\u8bbe\u5907\u4e0a\u7ebf'), (4, '\u8bbe\u5907\u4e0b\u7ebf'), (5, '\u5b9a\u671f\u7ef4\u62a4'), (6, '\u4e1a\u52a1\u4e0a\u7ebf\\\u66f4\u65b0\\\u53d8\u66f4'), (7, '\u5176\u5b83')], verbose_name='\u4e8b\u4ef6\u7c7b\u578b')),
                ('component', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4e8b\u4ef6\u5b50\u9879')),
                ('detail', models.TextField(verbose_name='\u4e8b\u4ef6\u8be6\u60c5')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u4e8b\u4ef6\u521b\u5efa\u65f6\u95f4')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u5907\u6ce8')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo')),
            ],
            options={
                'verbose_name': '\u4e8b\u4ef6',
                'verbose_name_plural': '\u4e8b\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'verbose_name': '\u673a\u623f',
                'verbose_name_plural': '\u673a\u623f',
            },
        ),
        migrations.CreateModel(
            name='Manufactory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='\u5382\u5546\u540d\u79f0')),
                ('support_num', models.CharField(blank=True, max_length=30, unique=True, verbose_name='\u670d\u52a1\u7535\u8bdd')),
                ('memo', models.TextField(blank=True, verbose_name='\u5907\u6ce8\u4fe1\u606f')),
            ],
            options={
                'verbose_name': '\u5382\u5546',
                'verbose_name_plural': '\u5382\u5546',
            },
        ),
        migrations.CreateModel(
            name='NetworkDeviceAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='\u7aef\u53e3\u6570\u91cf')),
                ('device_detail', models.TextField(blank=True, null=True, verbose_name='\u8bbe\u5907\u8be6\u60c5')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('asset_common_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo')),
            ],
            options={
                'verbose_name': '\u7f51\u7edc\u8bbe\u5907',
                'verbose_name_plural': '\u7f51\u7edc\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='\u8d44\u4ea7SN\u53f7')),
                ('asset_type', models.CharField(blank=True, choices=[(b'server', '\u670d\u52a1\u5668'), (b'switch', '\u4ea4\u6362\u673a'), (b'router', '\u8def\u7531\u5668'), (b'firewall', '\u9632\u706b\u5899'), (b'storage', '\u5b58\u50a8\u8bbe\u5907'), (b'wireless', '\u65e0\u7ebf\u8bbe\u5907'), (b'software', '\u8f6f\u4ef6\u8d44\u4ea7'), (b'other', '\u5176\u4ed6\u8d44\u4ea7')], max_length=64, null=True, verbose_name='\u8d44\u4ea7\u7c7b\u578b')),
                ('manufatory', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u5236\u9020\u5382\u5546')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u578b\u53f7')),
                ('ram_size', models.IntegerField(blank=True, null=True)),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True)),
                ('os_type', models.CharField(blank=True, max_length=64, null=True)),
                ('os_release', models.CharField(blank=True, max_length=64, null=True)),
                ('data', models.TextField(verbose_name='\u8d44\u4ea7\u6570\u636e')),
                ('report_date', models.DateTimeField(auto_now_add=True, verbose_name='\u6570\u636e\u6c47\u62a5\u65e5\u671f')),
                ('approved', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6279\u51c6')),
                ('approved_date', models.DateTimeField(blank=True, null=True, verbose_name='\u6279\u51c6\u65e5\u671f')),
            ],
            options={
                'verbose_name': '\u65b0\u4e0a\u7ebf\u5f85\u6279\u51c6\u8d44\u4ea7',
                'verbose_name_plural': '\u65b0\u4e0a\u7ebf\u5f85\u6279\u51c6\u8d44\u4ea7',
            },
        ),
        migrations.CreateModel(
            name='ServerAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(choices=[(b'auto', b'Auto'), (b'manual', b'Manual')], default=b'auto', max_length=32)),
                ('raid_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='raid\u7c7b\u578b')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('asset_common_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo')),
                ('hosted_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosted_on_server', to='assets.ServerAsset')),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668',
                'verbose_name_plural': '\u670d\u52a1\u5668',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(b'linux', b'Linux'), (b'windows', b'Windows'), (b'network_firmware', b'Network Firmware'), (b'software', b'Software')], default=1, help_text='eg.GNU/Linux', max_length=64, verbose_name='\u8f6f\u4ef6\u7c7b\u578b')),
                ('distribution', models.CharField(choices=[(b'windows', b'Windows'), (b'centos', b'Centos'), (b'ubuntu', b'Ubuntu')], default=b'windows', max_length=32, verbose_name='\u53d1\u884c\u7248\u672c')),
                ('version', models.CharField(max_length=32, unique=True, verbose_name='\u8f6f\u4ef6/\u7cfb\u7edf\u7248\u672c')),
                ('language', models.CharField(choices=[(b'cn', '\u4e2d\u6587'), (b'en', '\u82f1\u6587')], default=b'cn', max_length=32, verbose_name='\u8f6f\u4ef6/\u7cfb\u7edf\u8bed\u8a00')),
            ],
            options={
                'verbose_name': '\u8f6f\u4ef6/\u7cfb\u7edf',
                'verbose_name_plural': '\u8f6f\u4ef6/\u7cfb\u7edf',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name=b'Email address')),
                ('name', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('token', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='token')),
                ('department', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='\u90e8\u95e8')),
                ('telephone', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='\u56fa\u5b9a\u7535\u8bdd')),
                ('mobile', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='\u624b\u673a')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='\u5907\u6ce8')),
                ('date_join', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('valid_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u751f\u6548\u65f6\u95f4')),
                ('invalid_time', models.DateTimeField(blank=True, null=True, verbose_name='\u5931\u6548\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('component_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.Component')),
                ('cpu_count', models.SmallIntegerField(verbose_name='CPU\u7269\u7406\u4e2a\u6570')),
                ('cpu_core_count', models.SmallIntegerField(verbose_name='CPU\u6838\u4e2a\u6570')),
                ('frequency', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u4e3b\u9891')),
            ],
            options={
                'verbose_name': 'CPU\u90e8\u4ef6',
                'verbose_name_plural': 'CPU\u90e8\u4ef6',
            },
            bases=('assets.component',),
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('component_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.Component')),
                ('capacity', models.IntegerField(verbose_name='\u78c1\u76d8\u5bb9\u91cf(GB)')),
                ('iface_type', models.CharField(choices=[(b'SATA', b'SATA'), (b'SAS', b'SAS'), (b'SCSI', b'SCSI'), (b'SSD', b'SSD')], default=b'SAS', max_length=64, verbose_name='\u63a5\u53e3\u7c7b\u578b')),
            ],
            options={
                'verbose_name': '\u78c1\u76d8',
                'verbose_name_plural': '\u78c1\u76d8',
            },
            bases=('assets.component',),
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('component_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.Component')),
                ('mac_address', models.CharField(max_length=64, unique=True, verbose_name='\u7269\u7406\u5730\u5740')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('netmask', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u63a9\u7801')),
                ('bonding_ip', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u7ed1\u5b9aIP')),
            ],
            options={
                'verbose_name': '\u7f51\u5361',
                'verbose_name_plural': '\u7f51\u5361',
            },
            bases=('assets.component',),
        ),
        migrations.CreateModel(
            name='RaidAdaptor',
            fields=[
                ('component_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.Component')),
            ],
            options={
                'verbose_name': 'RaidAdaptor',
                'verbose_name_plural': 'RaidAdaptor',
            },
            bases=('assets.component',),
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('component_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.Component')),
                ('capacity', models.IntegerField(verbose_name='\u5185\u5b58\u5927\u5c0f(Mb)')),
            ],
            options={
                'verbose_name': 'RAM',
                'verbose_name_plural': 'RAM',
            },
            bases=('assets.component',),
        ),
        migrations.AddField(
            model_name='serverasset',
            name='os_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Software'),
        ),
        migrations.AddField(
            model_name='newassetapprovalzone',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile', verbose_name='\u6279\u51c6\u4eba'),
        ),
        migrations.AddField(
            model_name='networkdeviceasset',
            name='firmware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Software'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile', verbose_name='\u4e8b\u4ef6\u6e90'),
        ),
        migrations.AddField(
            model_name='component',
            name='manufatory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Manufactory'),
        ),
        migrations.AddField(
            model_name='assettag',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile'),
        ),
        migrations.AddField(
            model_name='assetcommoninfo',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.UserProfile', verbose_name='\u8d44\u4ea7\u7ba1\u7406\u5458'),
        ),
        migrations.AddField(
            model_name='assetcommoninfo',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.BusinessUnit', verbose_name='\u6240\u5c5e\u4e1a\u52a1\u7ebf'),
        ),
        migrations.AddField(
            model_name='assetcommoninfo',
            name='contract',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Contract', verbose_name='\u5408\u540c'),
        ),
        migrations.AddField(
            model_name='assetcommoninfo',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.IDC', verbose_name='\u6240\u5c5e\u673a\u623f'),
        ),
        migrations.AddField(
            model_name='assetcommoninfo',
            name='manufatory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Manufactory', verbose_name='\u5236\u9020\u5382\u5546'),
        ),
        migrations.AddField(
            model_name='ram',
            name='common_asset_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo'),
        ),
        migrations.AddField(
            model_name='raidadaptor',
            name='common_asset_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo'),
        ),
        migrations.AddField(
            model_name='nic',
            name='common_asset_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo'),
        ),
        migrations.AddField(
            model_name='disk',
            name='common_asset_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='asset_common_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetCommonInfo'),
        ),
    ]
