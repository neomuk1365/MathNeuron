from flask import Blueprint, jsonify, request
from app.models import Question, QuizAttempt, db

bp = Blueprint('api', __name__)

@bp.route('/questions/<int:topic_id>')
def get_questions(topic_id):
    questions = Question.query.filter_by(topic_id=topic_id).order_by(Question.difficulty).all()
    return jsonify([{
        'id': q.id,
        'type': q.type,
        'difficulty': q.difficulty,
        'question_text': q.question_text,
        'options': q.get_options(),
        'explanation': q.get_explanation(),
        # Intentionally leaving out correct_answer. The client will send the selected answer to verify, 
        # or for a purely client-side MVP we could include it, but let's do client side for instant feedback MVP.
        'correct_answer': q.correct_answer
    } for q in questions])

@bp.route('/submit_attempt', methods=['POST'])
def submit_attempt():
    data = request.json
    # In a real app with auth, we'd use current_user.id
    # For MVP without auth, we'll mock user_id = 1
    user_id = 1 
    
    attempt = QuizAttempt(
        user_id=user_id,
        question_id=data['question_id'],
        is_correct=data['is_correct'],
        selected_answer=data['selected_answer']
    )
    db.session.add(attempt)
    db.session.commit()
    
    return jsonify({'status': 'success'})
