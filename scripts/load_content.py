import json
import os
from pathlib import Path
from app import create_app, db
from app.models import Chapter, Topic, Question

def load_content():
    app = create_app()
    with app.app_context():
        # Clear existing for idempotency (in MVP)
        db.drop_all()
        db.create_all()

        content_dir = Path(__file__).resolve().parent.parent / 'content'
        
        for chapter_folder in sorted(os.listdir(content_dir)):
            folder_path = content_dir / chapter_folder
            if not folder_path.is_dir():
                continue
                
            theory_path = folder_path / 'theory.json'
            quiz_path = folder_path / 'quiz.json'
            
            if theory_path.exists():
                with open(theory_path, 'r', encoding='utf-8') as f:
                    theory_data = json.load(f)
                    
                chapter = Chapter(
                    slug=theory_data['chapter_slug'],
                    title=theory_data['title'],
                    order=theory_data['order'],
                    description=theory_data.get('description', ''),
                    is_published=True
                )
                db.session.add(chapter)
                db.session.flush() # Get chapter ID
                
                for topic_data in theory_data['topics']:
                    topic = Topic(
                        chapter_id=chapter.id,
                        title=topic_data['title'],
                        slug=topic_data['slug'],
                        order=topic_data['order'],
                        content_json=json.dumps(topic_data['content'])
                    )
                    db.session.add(topic)
                    db.session.flush() # Get topic ID
                    
                    # Try to load quiz for this topic
                    if quiz_path.exists():
                        with open(quiz_path, 'r', encoding='utf-8') as qf:
                            quiz_data = json.load(qf)
                            for q_data in quiz_data:
                                if q_data['topic_slug'] == topic.slug:
                                    question = Question(
                                        topic_id=topic.id,
                                        type=q_data.get('type', 'mcq'),
                                        difficulty=q_data.get('difficulty', 1),
                                        question_text=q_data['question_text'],
                                        options_json=json.dumps(q_data['options']),
                                        correct_answer=q_data['correct_answer'],
                                        explanation_json=json.dumps(q_data['explanation'])
                                    )
                                    db.session.add(question)
                                    
        db.session.commit()
        print("Content loaded successfully!")

if __name__ == '__main__':
    load_content()
