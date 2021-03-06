# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Faction'
        db.create_table('representative_faction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
        ))
        db.send_create_signal('representative', ['Faction'])

        # Deleting field 'Representative.faction_en'
        db.delete_column('representative_representative', 'faction_en')

        # Deleting field 'Representative.faction_ka'
        db.delete_column('representative_representative', 'faction_ka')


        # Renaming column for 'Representative.faction' to match new field type.
        db.rename_column('representative_representative', 'faction', 'faction_id')
        # Changing field 'Representative.faction'
        db.alter_column('representative_representative', 'faction_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['representative.Faction']))
        # Adding index on 'Representative', fields ['faction']
        db.create_index('representative_representative', ['faction_id'])

        # Removing M2M table for field parties on 'Cabinet'
        db.delete_table(db.shorten_name('representative_cabinet_parties'))

        # Adding M2M table for field factions on 'Cabinet'
        m2m_table_name = db.shorten_name('representative_cabinet_factions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cabinet', models.ForeignKey(orm['representative.cabinet'], null=False)),
            ('faction', models.ForeignKey(orm['representative.faction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cabinet_id', 'faction_id'])


    def backwards(self, orm):
        # Removing index on 'Representative', fields ['faction']
        db.delete_index('representative_representative', ['faction_id'])

        # Deleting model 'Faction'
        db.delete_table('representative_faction')

        # Adding field 'Representative.faction_en'
        db.add_column('representative_representative', 'faction_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Representative.faction_ka'
        db.add_column('representative_representative', 'faction_ka',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Renaming column for 'Representative.faction' to match new field type.
        db.rename_column('representative_representative', 'faction_id', 'faction')
        # Changing field 'Representative.faction'
        db.alter_column('representative_representative', 'faction', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding M2M table for field parties on 'Cabinet'
        m2m_table_name = db.shorten_name('representative_cabinet_parties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cabinet', models.ForeignKey(orm['representative.cabinet'], null=False)),
            ('party', models.ForeignKey(orm['representative.party'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cabinet_id', 'party_id'])

        # Removing M2M table for field factions on 'Cabinet'
        db.delete_table(db.shorten_name('representative_cabinet_factions'))


    models = {
        'popit.organisation': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Organisation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ended': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '300'}),
            'started': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'summary_ka': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'popit.person': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Person'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'date_of_death': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_ka': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'representative.additionalinformation': {
            'Meta': {'object_name': 'AdditionalInformation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'additional_information'", 'null': 'True', 'to': "orm['representative.Representative']"}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'value_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'value_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'representative.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'absent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'attended': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_absent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percentage_attended': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attendance'", 'to': "orm['representative.Representative']"}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'representative.cabinet': {
            'Meta': {'object_name': 'Cabinet'},
            'factions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'cabinet'", 'blank': 'True', 'to': "orm['representative.Faction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'representative.faction': {
            'Meta': {'object_name': 'Faction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'})
        },
        'representative.familyincome': {
            'Meta': {'object_name': 'FamilyIncome'},
            'ad_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'fam_cars': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fam_date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fam_gender': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fam_income': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'fam_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fam_role': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'family_income'", 'null': 'True', 'to': "orm['representative.Representative']"}),
            'submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'representative.party': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Party', '_ormbases': ['popit.Organisation']},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'organisation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['popit.Organisation']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'representative.randomrepresentative': {
            'Meta': {'object_name': 'RandomRepresentative'},
            'date_set': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representative.Representative']", 'null': 'True'})
        },
        'representative.representative': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Representative', '_ormbases': ['popit.Person']},
            'answered': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'committee': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'committee_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'committee_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_address_phone': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_address_phone_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_address_phone_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'declaration_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'education_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'education_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'elected': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'elected_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'elected_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'electoral_district': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'electoral_district_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'electoral_district_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entrepreneurial_salary': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'expenses': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expenses_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expenses_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'representatives'", 'null': 'True', 'to': "orm['representative.Faction']"}),
            'family_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'family_status_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'family_status_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'is_majoritarian': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_salary': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'other_income': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'representatives'", 'null': 'True', 'to': "orm['representative.Party']"}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['popit.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pob': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pob_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pob_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'property_assets': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'property_assets_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'property_assets_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'salary': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'terms': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'representatives'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['representative.Term']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'representatives'", 'null': 'True', 'to': "orm['representative.Unit']"})
        },
        'representative.term': {
            'Meta': {'object_name': 'Term'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'representative.unit': {
            'Meta': {'object_name': 'Unit'},
            'active_term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unit_active'", 'null': 'True', 'to': "orm['representative.Term']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inactive_terms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'unit_inactive'", 'blank': 'True', 'to': "orm['representative.Term']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parties': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'unit'", 'symmetrical': 'False', 'to': "orm['representative.Party']"}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'representative.url': {
            'Meta': {'object_name': 'Url'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u'Homepage'", 'max_length': '255'}),
            'label_en': ('django.db.models.fields.CharField', [], {'default': "u'Homepage'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'label_ka': ('django.db.models.fields.CharField', [], {'default': "u'Homepage'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'null': 'True', 'to': "orm['representative.Representative']"}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['representative']