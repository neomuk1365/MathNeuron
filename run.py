from app import create_app, db
from app.models import User, Chapter, Topic, Question, UserProgress, QuizAttempt

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Chapter': Chapter, 'Topic': Topic, 'Question': Question}

if __name__ == '__main__':
    app.run(debug=True)
