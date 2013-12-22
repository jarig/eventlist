# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FacilityType'
        db.create_table(u'blog_facilitytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blog', ['FacilityType'])

        # Adding unique constraint on 'FacilityType', fields ['name']
        db.create_unique(u'blog_facilitytype', ['name'])

        # Adding model 'BlogStyle'
        db.create_table(u'blog_blogstyle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'blog', ['BlogStyle'])

        # Adding model 'Blog'
        db.create_table(u'blog_blog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('logo', self.gf('_ext.pibu.fields.ImagePreviewModelField')(max_length=100, max_size=5368709120L, max_width=150, format='PNG')),
            ('type', self.gf('django.db.models.fields.CharField')(default='RR', max_length=2)),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('rating', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('style', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['blog.BlogStyle'])),
            ('fq_venue_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'blog', ['Blog'])

        # Adding M2M table for field facilities on 'Blog'
        m2m_table_name = db.shorten_name(u'blog_blog_facilities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm[u'blog.blog'], null=False)),
            ('facilitytype', models.ForeignKey(orm[u'blog.facilitytype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blog_id', 'facilitytype_id'])

        # Adding M2M table for field addresses on 'Blog'
        m2m_table_name = db.shorten_name(u'blog_blog_addresses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm[u'blog.blog'], null=False)),
            ('address', models.ForeignKey(orm[u'common.address'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blog_id', 'address_id'])

        # Adding model 'BlogAccess'
        db.create_table(u'blog_blogaccess', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Blog'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('access', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'blog', ['BlogAccess'])

        # Adding unique constraint on 'BlogAccess', fields ['blog', 'user', 'access']
        db.create_unique(u'blog_blogaccess', ['blog_id', 'user_id', 'access'])

        # Adding model 'BlogTip'
        db.create_table(u'blog_blogtip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Blog'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'blog', ['BlogTip'])


    def backwards(self, orm):
        # Removing unique constraint on 'BlogAccess', fields ['blog', 'user', 'access']
        db.delete_unique(u'blog_blogaccess', ['blog_id', 'user_id', 'access'])

        # Removing unique constraint on 'FacilityType', fields ['name']
        db.delete_unique(u'blog_facilitytype', ['name'])

        # Deleting model 'FacilityType'
        db.delete_table(u'blog_facilitytype')

        # Deleting model 'BlogStyle'
        db.delete_table(u'blog_blogstyle')

        # Deleting model 'Blog'
        db.delete_table(u'blog_blog')

        # Removing M2M table for field facilities on 'Blog'
        db.delete_table(db.shorten_name(u'blog_blog_facilities'))

        # Removing M2M table for field addresses on 'Blog'
        db.delete_table(db.shorten_name(u'blog_blog_addresses'))

        # Deleting model 'BlogAccess'
        db.delete_table(u'blog_blogaccess')

        # Deleting model 'BlogTip'
        db.delete_table(u'blog_blogtip')


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
        u'blog.blogtip': {
            'Meta': {'object_name': 'BlogTip'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']"}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Blog']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"})
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
        }
    }

    complete_apps = ['blog']