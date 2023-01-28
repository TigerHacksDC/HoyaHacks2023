from flask import Flask, render_template, redirect, url_for
from task import Task, tasks
from department import Department, departments
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aRandomString'


class EditTask(FlaskForm):
    select = SelectField('select', choices=[('Edit Task', 'Edit Task'), ('Delete Task', 'Delete Task')])
    field = StringField('field', validators=[InputRequired()])
    submit = SubmitField('Submit')

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
    edit = EditTask()
    if form.validate_on_submit():
        Task(name=form.name.data, description=form.description.data, department=form.department.data)
    return render_template('task.html', form=form, tasks=tasks, edit=edit)


# @app.route('/task/<task>')
# def task(task):
#     return str(tasks[int(task)].name)


@app.route('/departments')
def departments_list():
    return render_template('departments.html', departments=departments)


if __name__ == '__main__':
    app.run()
