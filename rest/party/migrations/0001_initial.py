# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Party'
        db.create_table(u'party_party', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='authorOfParties', to=orm['account.Account'])),
            ('logo', self.gf('_ext.pibu.fields.ImagePreviewModelField')(blank=True, max_length=100, null=True, max_size=5368709120L, format='PNG')),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('eventSchedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.EventSchedule'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('dateFrom', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('timeFrom', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('dateTo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('timeTo', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Event'], null=True, blank=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Blog'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Address'], null=True, blank=True)),
        ))
        db.send_create_signal(u'party', ['Party'])

        # Adding model 'PartyMember'
        db.create_table(u'party_partymember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(related_name='members', to=orm['party.Party'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partyMembership', to=orm['account.Account'])),
            ('role', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('invitedBy', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['account.Account'])),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'party', ['PartyMember'])

        # Adding unique constraint on 'PartyMember', fields ['party', 'user']
        db.create_unique(u'party_partymember', ['party_id', 'user_id'])

        # Adding model 'MemberVacancy'
        db.create_table(u'party_membervacancy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Event'])),
            ('age_min', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('age_max', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('hasPhoto', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Language'], null=True, blank=True)),
            ('num', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'party', ['MemberVacancy'])


    def backwards(self, orm):
        # Removing unique constraint on 'PartyMember', fields ['party', 'user']
        db.delete_unique(u'party_partymember', ['party_id', 'user_id'])

        # Deleting model 'Party'
        db.delete_table(u'party_party')

        # Deleting model 'PartyMember'
        db.delete_table(u'party_partymember')

        # Deleting model 'MemberVacancy'
        db.delete_table(u'party_membervacancy')


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
        u'common.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        },
        u'party.membervacancy': {
            'Meta': {'object_name': 'MemberVacancy'},
            'age_max': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_min': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Event']"}),
            'hasPhoto': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Language']", 'null': 'True', 'blank': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        u'party.party': {
            'Meta': {'object_name': 'Party'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Address']", 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authorOfParties'", 'to': u"orm['account.Account']"}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Blog']", 'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateFrom': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dateTo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Event']", 'null': 'True', 'blank': 'True'}),
            'eventSchedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.EventSchedule']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('_ext.pibu.fields.ImagePreviewModelField', [], {'blank': 'True', 'max_length': '100', 'null': 'True', 'max_size': '5368709120L', 'format': "'PNG'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeFrom': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'timeTo': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'party.partymember': {
            'Meta': {'unique_together': "(('party', 'user'),)", 'object_name': 'PartyMember'},
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitedBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['account.Account']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': u"orm['party.Party']"}),
            'role': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partyMembership'", 'to': u"orm['account.Account']"})
        }
    }

    complete_apps = ['party']