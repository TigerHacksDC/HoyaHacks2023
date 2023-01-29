from flask import Flask, render_template, redirect, url_for, request
from task import Task, tasks
from department import Department, departments, DepartmentForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)

app.config['SECRET_KEY'] = app.config.from_pyfile('config.py')

class EditTask(FlaskForm):
    hidden = HiddenField('hidden')
    select = SelectField('select', choices=[('Edit Name', 'Edit Name'), ('Delete Description', 'Description Task')])
    field = StringField('field', validators=[InputRequired()])
    submit = SubmitField('Submit')


class DeleteTask(FlaskForm):
    submit = SubmitField('Delete Task')


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
    delete = DeleteTask()
    if form.validate_on_submit() or edit.validate_on_submit() or delete.validate_on_submit():
        if form.validate():
            Task(name=form.name.data, description=form.description.data, department=form.department.data)
            return redirect(url_for('task'))

        elif edit.validate():
            if edit.select.data == 'Edit Name':
                tasks[int(request.form['index'])-1].name = edit.field.data
            else:
                tasks[int(request.form['index'])-1].description = edit.field.data
            return redirect(url_for('task'))
        elif delete.validate():
            tasks.pop(int(request.form['index'])-1)
            return redirect(url_for('task'))
    return render_template('task.html', form=form, tasks=tasks, edit=edit, delete=delete)


# @app.route('/task/<task>')
# def task(task):
#     return str(tasks[int(task)].name)


@app.route('/departments')
def departments_list():
    form = DepartmentForm()
    return render_template('departments.html', departments=departments, form=form)


if __name__ == '__main__':
    app.run()
