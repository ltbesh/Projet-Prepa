# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('QCM_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('key_expires', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('QCM', ['UserProfile'])

        # Adding model 'Subject'
        db.create_table('QCM_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('QCM', ['Subject'])

        # Adding model 'Level'
        db.create_table('QCM_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('QCM', ['Level'])

        # Adding model 'Chapter'
        db.create_table('QCM_chapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('QCM', ['Chapter'])

        # Adding model 'Question'
        db.create_table('QCM_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Level'], null=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Subject'], null=True)),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Chapter'], null=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 15, 0, 0))),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('QCM', ['Question'])

        # Adding model 'Quizz'
        db.create_table('QCM_quizz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_started', self.gf('django.db.models.fields.DateTimeField')()),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Level'], null=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Subject'], null=True)),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Chapter'], null=True)),
            ('grade', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('QCM', ['Quizz'])

        # Adding model 'QuestionStatus'
        db.create_table('QCM_questionstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Question'])),
            ('quizz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Quizz'])),
            ('answered', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('QCM', ['QuestionStatus'])

        # Adding model 'Answer'
        db.create_table('QCM_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Question'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('validity', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('QCM', ['Answer'])

        # Adding model 'Guess'
        db.create_table('QCM_guess', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quizz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Quizz'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QCM.Answer'])),
            ('answer_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('QCM', ['Guess'])

        # Adding model 'News'
        db.create_table('QCM_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('QCM', ['News'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('QCM_userprofile')

        # Deleting model 'Subject'
        db.delete_table('QCM_subject')

        # Deleting model 'Level'
        db.delete_table('QCM_level')

        # Deleting model 'Chapter'
        db.delete_table('QCM_chapter')

        # Deleting model 'Question'
        db.delete_table('QCM_question')

        # Deleting model 'Quizz'
        db.delete_table('QCM_quizz')

        # Deleting model 'QuestionStatus'
        db.delete_table('QCM_questionstatus')

        # Deleting model 'Answer'
        db.delete_table('QCM_answer')

        # Deleting model 'Guess'
        db.delete_table('QCM_guess')

        # Deleting model 'News'
        db.delete_table('QCM_news')


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
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Chapter']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Level']", 'null': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 15, 0, 0)'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['QCM.Subject']", 'null': 'True'})
        },
        'QCM.questionstatus': {
            'Meta': {'object_name': 'QuestionStatus'},
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
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['QCM.Question']", 'through': "orm['QCM.QuestionStatus']", 'symmetrical': 'False'}),
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