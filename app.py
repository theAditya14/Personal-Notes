from flask import Flask,redirect,render_template,url_for,request,flash
from models import db,Notes

app = Flask(__name__)   

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    notes = Notes.query.all()
    return render_template('home.html',notes=notes)

@app.route('/add_note',methods=['POST','GET'])
def add_note():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        new_note = Notes(title=title, content=content)

        db.session.add(new_note)
        db.session.commit()
        flash("Note added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_note.html')

@app.route('/edit_note/<int:id>',methods=['POST','GET'])
def edit_note(id):
    note = Notes.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        flash("Note updated successfully!", "success") 
        return redirect(url_for('home'))
    return render_template('edit_note.html',note=note)


@app.route('/delete/<int:id>')
def delete(id):
    note_delete = Notes.query.get_or_404(id)
    db.session.delete(note_delete)
    db.session.commit()
    flash(f" {id} deleted successfuly","success")
    return redirect(url_for('home'))

@app.route('/search')
def search():
    keyword = request.args.get('q')

    if keyword :
          results = Notes.query.filter(
              (Notes.title.contains(keyword)) |
              (Notes.content.contains(keyword)) 
              ).all()
          flash("This is your note..","sessuce")
          
    else:
          flash("Not Found!","empty")
          results = []

    return render_template('home.html',results=results,keyword=keyword)

if __name__== '__main__':
    app.run(debug=True)
















