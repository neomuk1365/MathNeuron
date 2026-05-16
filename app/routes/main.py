from flask import Blueprint, render_template, make_response, request
from app.models import Chapter

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template(
        'index.html',
        og_title="Math Intuition Platform | Master Data Science Mathematics",
        meta_description="A revolutionary platform teaching Mathematics for Data Science, Machine Learning, and Statistics. Build deep mathematical intuition instead of memorizing formulas.",
        meta_keywords="Data Science Math, Machine Learning Mathematics, Statistics, Probability, Math Intuition, Artificial Intelligence Mathematics"
    )

@bp.route('/learn')
def learn():
    chapters = Chapter.query.order_by(Chapter.order).all()
    return render_template('learn/index.html', chapters=chapters)

@bp.route('/learn/<slug>')
def chapter(slug):
    chapter = Chapter.query.filter_by(slug=slug).first_or_404()
    
    prev_chapter = Chapter.query.filter(Chapter.order < chapter.order).order_by(Chapter.order.desc()).first()
    next_chapter = Chapter.query.filter(Chapter.order > chapter.order).order_by(Chapter.order.asc()).first()
    
    return render_template(
        'learn/chapter.html', 
        chapter=chapter, 
        prev_chapter=prev_chapter, 
        next_chapter=next_chapter,
        og_title=f"{chapter.title} | Math Intuition for Data Science",
        meta_description=chapter.description or f"Master the intuition behind {chapter.title} for Machine Learning and Statistics.",
        meta_keywords=f"{chapter.title}, Data Science Math, Machine Learning Mathematics, Statistics Intuition"
    )

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

@bp.route('/robots.txt')
def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.url_root}sitemap.xml"
    ]
    response = make_response("\n".join(lines))
    response.headers["Content-Type"] = "text/plain"
    return response

@bp.route('/sitemap.xml')
def sitemap():
    chapters = Chapter.query.filter_by(is_published=True).order_by(Chapter.order).all()
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    # Add static routes
    static_urls = ['/', '/learn', '/practice']
    for url in static_urls:
        xml_lines.append(f"  <url>\n    <loc>{request.url_root.rstrip('/')}{url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>")
        
    # Add dynamic chapter routes
    for chapter in chapters:
        xml_lines.append(f"  <url>\n    <loc>{request.url_root}learn/{chapter.slug}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>")
        
    xml_lines.append('</urlset>')
    
    response = make_response("\n".join(xml_lines))
    response.headers["Content-Type"] = "application/xml"
    return response
