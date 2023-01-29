from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

departments = []


class Department:
    def __init__(self, name, members):
        self.name = name
        if members.__class__ == list:
            self.members = members
        else:
            self.members = [members]
        departments.append(self)


class DepartmentForm(FlaskForm):
    member = StringField('member', validators=[InputRequired(), Length(min=1, max=16)])
    submit = SubmitField('Add Department')
