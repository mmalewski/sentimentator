# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


class Language(db.Model):
    __tablename__ = 'language'
    _lid = db.Column('id', db.Integer, primary_key=True)
    _language = db.Column('language', db.String)

    def __init__(self, language):
        self._language = language

    @property
    def lid(self):
        return self._lid


class Sentence(db.Model):
    __tablename__ = 'sentence'
    _sid = db.Column('id', db.Integer, primary_key=True)
    _sentence = db.Column('sentence', db.String)
    _lid = db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
    _opus_sid = db.Column('opus_sid', db.Integer)
    _opus_did = db.Column('opus_did', db.String)

    def __init__(self, sentence, language_id, opus_did, opus_sid):
        self._sentence = sentence
        self._lid = language_id
        self._opus_did = opus_did
        self._opus_sid = opus_sid

    @property
    def sid(self):
        return self._sid

    def __str__(self):
        return self._sentence


class Annotation(db.Model):
    __tablename__ = 'annotation'
    _aid = db.Column('id', db.Integer, primary_key=True)
    _annotation = db.Column('annotation', db.String)
    _sid = db.Column('sentence_id', db.Integer, db.ForeignKey('sentence.id'))
    _uid = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    _intensity = db.Column('intensity', db.Float)

    # Annotation mode: traditional or intuitive.
    # TODO: Add to database.py functions to save these values to the db.
    _mode = db.Column('mode', db.String)
    # Whether the sentence is a seed sentence.
    # Save this to db based on annotator ID: expert annotator etc.
    _is_seed = db.Column('is_seed', db.Boolean)

    def __init__(self, annotation, sentence_id, user_id, intensity, mode, is_seed):
        self._annotation = annotation
        self._sid = sentence_id
        self._uid = user_id
        self._intensity = intensity
        self._mode = mode
        self._is_seed = is_seed

db.Index('ix_annotation_lookup', Annotation._sid, Annotation._uid)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    _uid = db.Column('id', db.Integer, primary_key=True)
    _user = db.Column('user', db.String)
    _pass = db.Column('pass', db.String)
    _rank = db.Column('rank', db.Float)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, username):
        self._user = username

    def __init__(self, username):
        self._user = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return self._uid

    def set_password(self, password):
        self._pass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._pass, password)

class Document(db.Model):
    __tablename__ = 'document'
    _did = db.Column('id', db.Integer, primary_key=True)
    _document = db.Column('document', db.String)

    @property
    def did(self):
        return self._did


class Alignment(db.Model):
    __tablename__ = 'alignment'
    _align_id = db.Column('alignment_id', db.Integer, primary_key=True)
    _lid1 = db.Column('lid1', db.Integer, db.ForeignKey('language.id'))
    _lid2 = db.Column('lid2', db.Integer, db.ForeignKey('language.id'))
    _did1 = db.Column('did1', db.Integer, db.ForeignKey('document.id'))
    _did2 = db.Column('did2', db.Integer, db.ForeignKey('document.id'))
    _sid1 = db.Column('sid1', db.Integer, db.ForeignKey('sentence.id'))
    _sid2 = db.Column('sid2', db.Integer, db.ForeignKey('sentence.id'))


db.Index('ix_alignment_lookup_1', Alignment._lid1, Alignment._lid2, Alignment._did1, Alignment._did2,
         Alignment._sid1, Alignment._sid2)
