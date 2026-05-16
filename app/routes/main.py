from flask import Blueprint, render_template
from app.models import Chapter

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/learn')
def learn():
    chapters = Chapter.query.order_by(Chapter.order).all()
    return render_template('learn/index.html', chapters=chapters)

@bp.route('/learn/<slug>')
def chapter(slug):
    chapter = Chapter.query.filter_by(slug=slug).first_or_404()
    
    prev_chapter = Chapter.query.filter(Chapter.order < chapter.order).order_by(Chapter.order.desc()).first()
    next_chapter = Chapter.query.filter(Chapter.order > chapter.order).order_by(Chapter.order.asc()).first()
    
    return render_template('learn/chapter.html', chapter=chapter, prev_chapter=prev_chapter, next_chapter=next_chapter)

@bp.route('/practice')
def practice():
    from app.models import Chapter, Topic, Question
    import json
    chapters = Chapter.query.order_by(Chapter.order).all()
    
    practice_data = []
    all_questions_by_topic = {}
    
    for chapter in chapters:
        chapter_data = {'title': chapter.title, 'topics': []}
        for topic in chapter.topics:
            questions = Question.query.filter_by(topic_id=topic.id).order_by(Question.difficulty).all()
            if questions:
                chapter_data['topics'].append({
                    'id': topic.id,
                    'title': topic.title,
                    'count': len(questions)
                })
                all_questions_by_topic[topic.id] = [{
                    'id': q.id,
                    'type': q.type,
                    'difficulty': q.difficulty,
                    'question_text': q.question_text,
                    'options': q.get_options(),
                    'explanation': q.get_explanation(),
                    'correct_answer': q.correct_answer
                } for q in questions]
        if chapter_data['topics']:
            practice_data.append(chapter_data)
            
    return render_template('practice/index.html', practice_data=practice_data, all_questions_by_topic=json.dumps(all_questions_by_topic))

@bp.route('/dashboard')
def dashboard():
    from app.models import QuizAttempt, Chapter
    user_id = 1 # mocked for MVP
    
    # Calculate stats
    total_attempts = QuizAttempt.query.filter_by(user_id=user_id).count()
    correct_attempts = QuizAttempt.query.filter_by(user_id=user_id, is_correct=True).count()
    
    # Assuming 10 XP per correct intuition check
    xp = correct_attempts * 10
    
    # Let's say a chapter is completed if they attempted at least 1 question in it (simplified for MVP)
    # Or just return 0 for chapters completed for now, and focus on correct attempts.
    
    return render_template('dashboard/index.html', 
                           correct_attempts=correct_attempts,
                           total_attempts=total_attempts,
                           xp=xp)
