import json
from datetime import datetime
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    streak = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    
    progress = db.relationship('UserProgress', backref='user', lazy='dynamic')
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), index=True, unique=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    
    topics = db.relationship('Topic', backref='chapter', lazy='dynamic', order_by='Topic.order')

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(64), index=True, nullable=False)
    content_json = db.Column(db.Text, nullable=False) # Store rich content structure
    order = db.Column(db.Integer, nullable=False)
    
    questions = db.relationship('Question', backref='topic', lazy='dynamic')

    def get_content(self):
        return json.loads(self.content_json)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    type = db.Column(db.String(32), default='mcq') # mcq, fill_in_blank, etc.
    difficulty = db.Column(db.Integer, default=1) # 1 (Beginner) to 6 (ML App)
    question_text = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text, nullable=False) # JSON array of options
    correct_answer = db.Column(db.String(128), nullable=False)
    explanation_json = db.Column(db.Text, nullable=False) # Contains 'intuition', 'common_mistakes', 'step_by_step'

    def get_options(self):
        return json.loads(self.options_json)
        
    def get_explanation(self):
        return json.loads(self.explanation_json)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    status = db.Column(db.String(32), default='started') # started, completed, struggling
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    selected_answer = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
