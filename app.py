from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>My Notes App</title></head>
<body>
    <h1>My Notes Application</h1>
    <form method="POST" action="/notes">
        <input name="title" placeholder="Title" required>
        <textarea name="content" placeholder="Content" required></textarea>
        <button type="submit">Add Note</button>
    </form>
    <hr>
    <form method="GET" action="/search">
        <input name="q" placeholder="Search notes">
        <button type="submit">Search</button>
    </form>
    <hr>
    <h2>All Notes</h2>
    <ul>
    {% for note in notes %}
        <li><strong>{{ note.title }}</strong>: {{ note.content }}</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def home():
    notes = Note.query.all()
    return render_template_string(HOME_TEMPLATE, notes=notes)

@app.route('/notes', methods=['POST'])
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')
    note = Note(title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return jsonify({'status': 'created', 'id': note.id}), 201

@app.route('/search')
def search():
    query = request.args.get('q', '')
    sql = f"SELECT * FROM note WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
    results = db.session.execute(sql)
    notes = [{'id': r[0], 'title': r[1], 'content': r[2]} for r in results]
    return jsonify(notes)

@app.route('/health')
def health():
    return jsonify({'status': 'UP'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
