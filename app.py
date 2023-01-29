from flask import Flask, render_template, redirect, url_for, request
from task import Task, tasks_list
from department import Department, departments_list, DepartmentForm, contains_member, contains_department_name
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SecretKeysAreUnnecessaryForThisProjectButWeHaveToHaveOneAnyways'


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


class DepartmentForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=1, max=16)])
    submit = SubmitField('Add Department')


class EditDepartment(FlaskForm):
    hidden = HiddenField('hidden')
    select = SelectField('select', choices=[('Edit Name', 'Edit Name'),
                                            ('Add Member', 'Add Member'),
                                            ('Delete Member', 'Delete Member')])
    field = StringField('field', validators=[InputRequired(), Length(min=1, max=16)])
    submit = SubmitField('Submit')


class DeleteDepartment(FlaskForm):
    submit = SubmitField('Delete Department')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task', methods=['GET', 'POST'])
def task():
    errors = []
    form = TaskForm()
    edit = EditTask()
    delete = DeleteTask()
    if form.validate_on_submit() or edit.validate_on_submit() or delete.validate_on_submit():
        if form.validate():
            Task(name=form.name.data, description=form.description.data, department=form.department.data)
            return redirect(url_for('task'))
        elif edit.validate():
            if edit.select.data == 'Edit Name':
                tasks_list[int(request.form['index']) - 1].name = edit.field.data
            else:
                tasks_list[int(request.form['index']) - 1].description = edit.field.data
            return redirect(url_for('task'))
        elif delete.validate():
            tasks_list.pop(int(request.form['index']) - 1)
            return redirect(url_for('task'))
    return render_template('task.html', form=form, tasks=tasks_list, edit=edit, delete=delete, errors=errors)


@app.route('/departments', methods=['GET', 'POST'])
def departments():
    errors = []
    form = DepartmentForm()
    edit = EditDepartment()
    delete = DeleteDepartment()
    if form.validate_on_submit() or edit.validate_on_submit() or delete.validate_on_submit():
        if form.validate():
            if not contains_department_name(form.name.data):
                Department(name=form.name.data, members=[])
                return redirect(url_for('departments'))
            else:
                errors.append('Department name already exists')
        elif edit.validate():
            if edit.select.data == 'Edit Name':
                departments_list[int(request.form['index']) - 1].name = edit.field.data
            elif edit.select.data == 'Add Member':
                departments_list[int(request.form['index']) - 1].members.append(edit.field.data)
            else:
                if contains_member(edit.field.data):
                    departments_list[int(request.form['index']) - 1].members.remove(edit.field.data)
            return redirect(url_for('departments'))
        elif delete.validate():
            departments_list.pop(int(request.form['index']) - 1)
            return redirect(url_for('departments'))
    return render_template('departments.html', form=form, departments=departments_list, edit=edit, delete=delete, errors=errors)


if __name__ == '__main__':
    app.run()
