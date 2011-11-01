# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'EventActivity'
        db.create_table('event_eventactivity', (
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('event', ['EventActivity'])

        # Adding model 'Event'
        db.create_table('event_event', (
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('timeFrom', self.gf('django.db.models.fields.TimeField')(default='00:00')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descr', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('dateTo', self.gf('django.db.models.fields.DateField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dateFrom', self.gf('django.db.models.fields.DateField')()),
            ('timeTo', self.gf('django.db.models.fields.TimeField')(default='00:00')),
            ('participants', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('event', ['Event'])

        # Adding M2M table for field activities on 'Event'
        db.create_table('event_event_activities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['event.event'], null=False)),
            ('eventactivity', models.ForeignKey(orm['event.eventactivity'], null=False))
        ))
        db.create_unique('event_event_activities', ['event_id', 'eventactivity_id'])

        # Adding M2M table for field blogs on 'Event'
        db.create_table('event_event_blogs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['event.event'], null=False)),
            ('blog', models.ForeignKey(orm['blogs.blog'], null=False))
        ))
        db.create_unique('event_event_blogs', ['event_id', 'blog_id'])

        # Adding M2M table for field addresses on 'Event'
        db.create_table('event_event_addresses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['event.event'], null=False)),
            ('address', models.ForeignKey(orm['common.address'], null=False))
        ))
        db.create_unique('event_event_addresses', ['event_id', 'address_id'])

        # Adding model 'Comment'
        db.create_table('event_comment', (
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Event'])),
        ))
        db.send_create_signal('event', ['Comment'])

        # Adding model 'Invite'
        db.create_table('event_invite', (
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invited', to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invites', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Event'])),
        ))
        db.send_create_signal('event', ['Invite'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'EventActivity'
        db.delete_table('event_eventactivity')

        # Deleting model 'Event'
        db.delete_table('event_event')

        # Removing M2M table for field activities on 'Event'
        db.delete_table('event_event_activities')

        # Removing M2M table for field blogs on 'Event'
        db.delete_table('event_event_blogs')

        # Removing M2M table for field addresses on 'Event'
        db.delete_table('event_event_addresses')

        # Deleting model 'Comment'
        db.delete_table('event_comment')

        # Deleting model 'Invite'
        db.delete_table('event_invite')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'blogs.blog': {
            'Meta': {'object_name': 'Blog'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['common.Address']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'facilities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blogs.FacilityType']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['blogs.BlogAccess']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['blogs.BlogStyle']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'RR'", 'max_length': '2'})
        },
        'blogs.blogaccess': {
            'Meta': {'unique_together': "(('blog', 'user', 'access'),)", 'object_name': 'BlogAccess'},
            'access': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blogs.Blog']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'blogs.blogstyle': {
            'Meta': {'object_name': 'BlogStyle'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'blogs.facilitytype': {
            'Meta': {'object_name': 'FacilityType'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100'})
        },
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'event.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['event.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        },
        'event.event': {
            'Meta': {'object_name': 'Event'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['event.EventActivity']", 'null': 'True', 'blank': 'True'}),
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['common.Address']", 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'blogs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blogs.Blog']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateFrom': ('django.db.models.fields.DateField', [], {}),
            'dateTo': ('django.db.models.fields.DateField', [], {}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'participants': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'timeFrom': ('django.db.models.fields.TimeField', [], {'default': "'00:00'"}),
            'timeTo': ('django.db.models.fields.TimeField', [], {'default': "'00:00'"})
        },
        'event.eventactivity': {
            'Meta': {'object_name': 'EventActivity'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'event.invite': {
            'Meta': {'object_name': 'Invite'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['event.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invited'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invites'", 'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['event']
