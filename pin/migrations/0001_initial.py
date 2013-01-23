# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table('pin_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')(default=1347546432, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('like', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('pin', ['Post'])

        # Adding model 'Follow'
        db.create_table('pin_follow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('follower', self.gf('django.db.models.fields.related.ForeignKey')(related_name='follower', to=orm['auth.User'])),
            ('following', self.gf('django.db.models.fields.related.ForeignKey')(related_name='following', to=orm['auth.User'])),
        ))
        db.send_create_signal('pin', ['Follow'])

        # Adding model 'Stream'
        db.create_table('pin_stream', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('following', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stream_following', to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pin.Post'])),
            ('date', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('pin', ['Stream'])

        # Adding model 'Likes'
        db.create_table('pin_likes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pin_post_user_like', to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_item', to=orm['pin.Post'])),
        ))
        db.send_create_signal('pin', ['Likes'])

        # Adding unique constraint on 'Likes', fields ['post', 'user']
        db.create_unique('pin_likes', ['post_id', 'user_id'])

        # Adding model 'Notify'
        db.create_table('pin_notify', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pin.Post'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='userid', to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('seen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('pin', ['Notify'])


    def backwards(self, orm):
        # Removing unique constraint on 'Likes', fields ['post', 'user']
        db.delete_unique('pin_likes', ['post_id', 'user_id'])

        # Deleting model 'Post'
        db.delete_table('pin_post')

        # Deleting model 'Follow'
        db.delete_table('pin_follow')

        # Deleting model 'Stream'
        db.delete_table('pin_stream')

        # Deleting model 'Likes'
        db.delete_table('pin_likes')

        # Deleting model 'Notify'
        db.delete_table('pin_notify')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pin.follow': {
            'Meta': {'object_name': 'Follow'},
            'follower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follower'", 'to': "orm['auth.User']"}),
            'following': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'following'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pin.likes': {
            'Meta': {'unique_together': "(('post', 'user'),)", 'object_name': 'Likes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_item'", 'to': "orm['pin.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pin_post_user_like'", 'to': "orm['auth.User']"})
        },
        'pin.notify': {
            'Meta': {'object_name': 'Notify'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pin.Post']"}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': "orm['auth.User']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userid'", 'to': "orm['auth.User']"})
        },
        'pin.post': {
            'Meta': {'object_name': 'Post'},
            'create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1347546432', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'pin.stream': {
            'Meta': {'object_name': 'Stream'},
            'date': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stream_following'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pin.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user'", 'to': "orm['auth.User']"})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['pin']