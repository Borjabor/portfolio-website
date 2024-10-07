from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'projects.db')
db = SQLAlchemy(app)

class Project(db.Model):
    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    title: Mapped[str] = mapped_column(Column(String(100), nullable=False))
    summary: Mapped[str] = mapped_column(Column(Text, nullable=False))
    images: Mapped[list["Image"]] = mapped_column(
        relationship("Image", backref="project", lazy=True)
    )
    videos: Mapped[list["Video"]] = mapped_column(
        relationship("Video", backref="project", lazy=True)
    )

class Image(db.Model):
    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    project_id: Mapped[int] = mapped_column(
        Column(Integer, ForeignKey("project.id"), nullable=False)
    )
    url: Mapped[str] = mapped_column(Column(String(200), nullable=False))

class Video(db.Model):
    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    project_id: Mapped[int] = mapped_column(
        Column(Integer, ForeignKey("project.id"), nullable=False)
    )
    url: Mapped[str] = mapped_column(Column(String(200), nullable=False))

with app.app_context():
    db.create_all()
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')


if __name__ == '__main__':
    app.run(debug=True)