# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'City'
        db.create_table('common_city', (
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Country'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('common', ['City'])

        # Adding field 'Country.rating'
        db.add_column('common_country', 'rating', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Renaming column for 'Address.city' to match new field type.
        db.rename_column('common_address', 'city', 'city_id')
        # Changing field 'Address.city'
        db.alter_column('common_address', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.City']))

        # Adding index on 'Address', fields ['city']
        db.create_index('common_address', ['city_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'City'
        db.delete_table('common_city')

        # Deleting field 'Country.rating'
        db.delete_column('common_country', 'rating')

        # Renaming column for 'Address.city' to match new field type.
        db.rename_column('common_address', 'city_id', 'city')
        # Changing field 'Address.city'
        db.alter_column('common_address', 'city', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Removing index on 'Address', fields ['city']
        db.delete_index('common_address', ['city_id'])
    
    
    models = {
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.City']"}),
            'cityArea': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Country']"}),
            'county': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'common.city': {
            'Meta': {'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'common.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'rating': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['common']
