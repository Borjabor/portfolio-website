from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '2NH9B7FCLp2jGwrJmgdmDYIOHq0OQCsR'
Bootstrap5(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'projects.db')
db = SQLAlchemy(app)

class Project(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str] = mapped_column(String(250), nullable=False)
    thumbnail: Mapped[str] = mapped_column(String(250), nullable=False)
    # images: Mapped[list["Image"]] = relationship("Image", backref="project", lazy=True)
    # videos: Mapped[list["Video"]] = relationship("Video", backref="project", lazy=True)

class Image(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("project.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)

class Video(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("project.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()
    
@app.route('/')
def home():
    result = db.session.execute(db.select(Project))
    projects = result.scalars().all() 
    return render_template('index.html', title="Andre Borja Miranda", projects=projects)

@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")


if __name__ == '__main__':
    app.run(debug=True)