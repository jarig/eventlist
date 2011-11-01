# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('common_country', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('common', ['Country'])

        # Adding model 'Address'
        db.create_table('common_address', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Country'])),
            ('cityArea', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('county', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postalCode', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('common', ['Address'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('common_country')

        # Deleting model 'Address'
        db.delete_table('common_address')
    
    
    models = {
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'cityArea': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Country']"}),
            'county': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'common.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }
    
    complete_apps = ['common']
