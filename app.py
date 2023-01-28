from flask import Flask, render_template, redirect, url_for
from task import Task
import task as task
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aRandomString'

task1 = Task('Task 1', 'This is task 1', 'Task')


# Form for adding tasks
class TaskForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=1, max=16)])
    description = StringField('description', validators=[InputRequired()])
    department = StringField('department', validators=[InputRequired()])
    submit = SubmitField('Add Task')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task', methods=['GET', 'POST'])
def task():
    form = TaskForm()
    if form.validate_on_submit():
        Task(name=form.name.data, description=form.description.data, department=form.department.data)
    return render_template('task.html', form=form, tasks=task.tasks)


if __name__ == '__main__':
    app.run()
