# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('jmbo_twitter_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('profile_image_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('jmbo_twitter', ['Feed'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('jmbo_twitter_feed')


    models = {
        'jmbo_twitter.feed': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Feed'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'profile_image_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['jmbo_twitter']