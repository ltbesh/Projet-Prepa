# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Question_statut'
        db.delete_table('QCM_question_statut')

        # Adding model 'QuestionStatut'
        db.create_table('QCM_questionstatut', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Question'])),
            ('quizz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Quizz'])),
            ('answered', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('QCM', ['QuestionStatut'])


    def backwards(self, orm):
        # Adding model 'Question_statut'
        db.create_table('QCM_question_statut', (
            ('answered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Question'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quizz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Quizz'])),
        ))
        db.send_create_signal('QCM', ['Question_statut'])

        # Deleting model 'QuestionStatut'
        db.delete_table('QCM_questionstatut')


    models = {
        'QCM.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Question']"}),
            'validity': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'QCM.chapter': {
            'Meta': {'object_name': 'Chapter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'QCM.guess': {
            'Meta': {'object_name': 'Guess'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Answer']"}),
            'answer_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quizz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Quizz']"})
        },
        'QCM.level': {
            'Meta': {'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'QCM.news': {
            'Meta': {'object_name': 'News'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'QCM.question': {
            'Meta': {'object_name': 'Question'},
            'chapter': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['QCM.Chapter']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['QCM.Level']", 'symmetrical': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 22, 0, 0)'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['QCM.Subject']", 'symmetrical': 'False'})
        },
        'QCM.questionstatut': {
            'Meta': {'object_name': 'QuestionStatut'},
            'answered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Question']"}),
            'quizz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Quizz']"})
        },
        'QCM.quizz': {
            'Meta': {'object_name': 'Quizz'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Chapter']", 'null': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Level']", 'null': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['QCM.Question']", 'through': "orm['QCM.QuestionStatut']", 'symmetrical': 'False'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Subject']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'QCM.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'QCM.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
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
        }
    }

    complete_apps = ['QCM']