# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Comments.text'
        db.delete_column('pin_comments', 'text')

        # Deleting field 'Comments.date'
        db.delete_column('pin_comments', 'date')

        # Deleting field 'Comments.ip'
        db.delete_column('pin_comments', 'ip')

        # Deleting field 'Comments.post'
        db.delete_column('pin_comments', 'post_id')

        # Deleting field 'Comments.public'
        db.delete_column('pin_comments', 'public')

        # Adding field 'Comments.comment'
        db.add_column('pin_comments', 'comment',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Comments.submit_date'
        db.add_column('pin_comments', 'submit_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 18, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Comments.ip_address'
        db.add_column('pin_comments', 'ip_address',
                      self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15),
                      keep_default=False)

        # Adding field 'Comments.is_public'
        db.add_column('pin_comments', 'is_public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Comments.object_pk'
        db.add_column('pin_comments', 'object_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='comment_post', to=orm['pin.Post']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Comments.text'
        raise RuntimeError("Cannot reverse this migration. 'Comments.text' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Comments.date'
        raise RuntimeError("Cannot reverse this migration. 'Comments.date' and its values cannot be restored.")
        # Adding field 'Comments.ip'
        db.add_column('pin_comments', 'ip',
                      self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Comments.post'
        raise RuntimeError("Cannot reverse this migration. 'Comments.post' and its values cannot be restored.")
        # Adding field 'Comments.public'
        db.add_column('pin_comments', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Comments.comment'
        db.delete_column('pin_comments', 'comment')

        # Deleting field 'Comments.submit_date'
        db.delete_column('pin_comments', 'submit_date')

        # Deleting field 'Comments.ip_address'
        db.delete_column('pin_comments', 'ip_address')

        # Deleting field 'Comments.is_public'
        db.delete_column('pin_comments', 'is_public')

        # Deleting field 'Comments.object_pk'
        db.delete_column('pin_comments', 'object_pk_id')


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
        'pin.app_data': {
            'Meta': {'object_name': 'App_data'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'pin.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'pin.comments': {
            'Meta': {'object_name': 'Comments'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_post'", 'to': "orm['pin.Post']"}),
            'reported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_sender'", 'to': "orm['auth.User']"})
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
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_item'", 'to': "orm['pin.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pin_post_user_like'", 'to': "orm['auth.User']"})
        },
        'pin.notif': {
            'Meta': {'object_name': 'Notif'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pin.Post']"}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_id'", 'to': "orm['auth.User']"})
        },
        'pin.notif_actors': {
            'Meta': {'object_name': 'Notif_actors'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notif': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notif'", 'to': "orm['pin.Notif']"})
        },
        'pin.notify': {
            'Meta': {'object_name': 'Notify'},
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'actors'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pin.Post']"}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userid'", 'to': "orm['auth.User']"})
        },
        'pin.post': {
            'Meta': {'object_name': 'Post'},
            'actions': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['pin.Category']"}),
            'create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'is_ads': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'show_in_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1347546432', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'view': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        'pin.stream': {
            'Meta': {'unique_together': "(('following', 'user', 'post'),)", 'object_name': 'Stream'},
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