# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventGroup'
        db.create_table(u'event_eventgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('popularity', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'event', ['EventGroup'])

        # Adding model 'EventActivity'
        db.create_table(u'event_eventactivity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
            ('thumbnail_128', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subActivities', null=True, to=orm['event.EventActivity'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='activities', null=True, to=orm['event.EventGroup'])),
        ))
        db.send_create_signal(u'event', ['EventActivity'])

        # Adding unique constraint on 'EventActivity', fields ['name']
        db.create_unique(u'event_eventactivity', ['name'])

        # Adding model 'Event'
        db.create_table(u'event_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('logo', self.gf('_ext.pibu.fields.ImagePreviewModelField')(max_size=5368709120L, max_length=100, max_height=300, max_width=300, format='PNG')),
            ('descr', self.gf('django.db.models.fields.TextField')()),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('participants', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'event', ['Event'])

        # Adding M2M table for field blogs on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_blogs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('blog', models.ForeignKey(orm[u'blog.blog'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'blog_id'])

        # Adding M2M table for field activities on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_activities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('eventactivity', models.ForeignKey(orm[u'event.eventactivity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'eventactivity_id'])

        # Adding M2M table for field organizers on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_organizers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('organization', models.ForeignKey(orm[u'organization.organization'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'organization_id'])

        # Adding model 'EventSchedule'
        db.create_table(u'event_eventschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['event.Event'])),
            ('dateFrom', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('timeFrom', self.gf('django.db.models.fields.TimeField')(default='00:00')),
            ('dateTo', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, null=True, blank=True)),
            ('timeTo', self.gf('django.db.models.fields.TimeField')(default='00:00', null=True, blank=True)),
            ('shortDescription', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eventSchedules', null=True, to=orm['common.Address'])),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='eventSchedules', null=True, blank=True, to=orm['blog.Blog'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['EventSchedule'])

        # Adding model 'EventTerms'
        db.create_table(u'event_eventterms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='terms', to=orm['event.Event'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='P', max_length=2)),
            ('min_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('classifier', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['EventTerms'])

        # Adding model 'EventGo'
        db.create_table(u'event_eventgo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eventSchedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.EventSchedule'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='goesOnEvents', to=orm['account.Account'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['EventGo'])

        # Adding unique constraint on 'EventGo', fields ['eventSchedule', 'user']
        db.create_unique(u'event_eventgo', ['eventSchedule_id', 'user_id'])

        # Adding model 'Comment'
        db.create_table(u'event_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Event'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['Comment'])

        # Adding model 'Invite'
        db.create_table(u'event_invite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Event'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invites', to=orm['account.Account'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invited', to=orm['account.Account'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['Invite'])

        # Adding unique constraint on 'Invite', fields ['event', 'user', 'person']
        db.create_unique(u'event_invite', ['event_id', 'user_id', 'person_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Invite', fields ['event', 'user', 'person']
        db.delete_unique(u'event_invite', ['event_id', 'user_id', 'person_id'])

        # Removing unique constraint on 'EventGo', fields ['eventSchedule', 'user']
        db.delete_unique(u'event_eventgo', ['eventSchedule_id', 'user_id'])

        # Removing unique constraint on 'EventActivity', fields ['name']
        db.delete_unique(u'event_eventactivity', ['name'])

        # Deleting model 'EventGroup'
        db.delete_table(u'event_eventgroup')

        # Deleting model 'EventActivity'
        db.delete_table(u'event_eventactivity')

        # Deleting model 'Event'
        db.delete_table(u'event_event')

        # Removing M2M table for field blogs on 'Event'
        db.delete_table(db.shorten_name(u'event_event_blogs'))

        # Removing M2M table for field activities on 'Event'
        db.delete_table(db.shorten_name(u'event_event_activities'))

        # Removing M2M table for field organizers on 'Event'
        db.delete_table(db.shorten_name(u'event_event_organizers'))

        # Deleting model 'EventSchedule'
        db.delete_table(u'event_eventschedule')

        # Deleting model 'EventTerms'
        db.delete_table(u'event_eventterms')

        # Deleting model 'EventGo'
        db.delete_table(u'event_eventgo')

        # Deleting model 'Comment'
        db.delete_table(u'event_comment')

        # Deleting model 'Invite'
        db.delete_table(u'event_invite')


    models = {
        u'account.account': {
            'Meta': {'unique_together': "(('identity', 'provider'),)", 'object_name': 'Account', '_ormbases': [u'auth.User']},
            'age': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('_ext.pibu.fields.ImagePreviewModelField', [], {'format': "'PNG'", 'default': "''", 'max_width': '164', 'max_length': '255', 'blank': 'True', 'null': 'True', 'max_size': '5368709120L'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.Account']", 'through': u"orm['account.FriendShip']", 'symmetrical': 'False'}),
            'identity': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': "'nt'", 'max_length': '128'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'account.friendship': {
            'Meta': {'unique_together': "(('creator', 'friend'),)", 'object_name': 'FriendShip'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['account.Account']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscribers'", 'to': u"orm['account.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'blog.blog': {
            'Meta': {'object_name': 'Blog'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['common.Address']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'facilities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['blog.FacilityType']", 'null': 'True', 'blank': 'True'}),
            'fq_venue_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('_ext.pibu.fields.ImagePreviewModelField', [], {'max_length': '100', 'max_size': '5368709120L', 'max_width': '150', 'format': "'PNG'"}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.Account']", 'through': u"orm['blog.BlogAccess']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['blog.BlogStyle']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'RR'", 'max_length': '2'})
        },
        u'blog.blogaccess': {
            'Meta': {'unique_together': "(('blog', 'user', 'access'),)", 'object_name': 'BlogAccess'},
            'access': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Blog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']"})
        },
        u'blog.blogstyle': {
            'Meta': {'object_name': 'BlogStyle'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'blog.facilitytype': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'FacilityType'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100'})
        },
        u'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.City']"}),
            'cityArea': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Country']"}),
            'county': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True'})
        },
        u'common.city': {
            'Meta': {'object_name': 'City'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'common.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'event.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        },
        u'event.event': {
            'Meta': {'object_name': 'Event'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['event.EventActivity']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']"}),
            'blogs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['blog.Blog']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('_ext.pibu.fields.ImagePreviewModelField', [], {'max_size': '5368709120L', 'max_length': '100', 'max_height': '300', 'max_width': '300', 'format': "'PNG'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'organizers'", 'symmetrical': 'False', 'to': u"orm['organization.Organization']"}),
            'participants': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'event.eventactivity': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'EventActivity'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'to': u"orm['event.EventGroup']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subActivities'", 'null': 'True', 'to': u"orm['event.EventActivity']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'thumbnail_128': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        u'event.eventgo': {
            'Meta': {'unique_together': "(('eventSchedule', 'user'),)", 'object_name': 'EventGo'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'eventSchedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.EventSchedule']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goesOnEvents'", 'to': u"orm['account.Account']"})
        },
        u'event.eventgroup': {
            'Meta': {'object_name': 'EventGroup'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'popularity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'event.eventschedule': {
            'Meta': {'object_name': 'EventSchedule'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventSchedules'", 'null': 'True', 'to': u"orm['common.Address']"}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'eventSchedules'", 'null': 'True', 'blank': 'True', 'to': u"orm['blog.Blog']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateFrom': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'dateTo': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'shortDescription': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'timeFrom': ('django.db.models.fields.TimeField', [], {'default': "'00:00'"}),
            'timeTo': ('django.db.models.fields.TimeField', [], {'default': "'00:00'", 'null': 'True', 'blank': 'True'})
        },
        u'event.eventterms': {
            'Meta': {'object_name': 'EventTerms'},
            'classifier': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '2'})
        },
        u'event.invite': {
            'Meta': {'unique_together': "(('event', 'user', 'person'),)", 'object_name': 'Invite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invited'", 'to': u"orm['account.Account']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invites'", 'to': u"orm['account.Account']"})
        },
        u'organization.orgaccess': {
            'Meta': {'unique_together': "(('member', 'organization', 'level'),)", 'object_name': 'OrgAccess'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"})
        },
        u'organization.organization': {
            'Meta': {'object_name': 'Organization'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Address']"}),
            'businessCode': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('_ext.pibu.fields.ImagePreviewModelField', [], {'max_length': '100', 'max_size': '5368709120L', 'max_width': '160', 'format': "'PNG'"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.Account']", 'through': u"orm['organization.OrgAccess']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['event']