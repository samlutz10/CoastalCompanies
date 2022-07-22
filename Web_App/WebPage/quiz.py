from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms.validators import ValidationError
from random import randrange


class CorrectAnswer(object):
    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        message = 'Incorrect answer.'

        if field.data != self.answer:
            raise ValidationError(message)


class PopQuiz(Form):
    class Meta:
        csrf = False
    q1 = RadioField(
        "True or False: When the hitch lock on the top of the trailer coupler is down, it is ready to recieve the ball.",
        choices=[('True'), ('False')],
        validators=[CorrectAnswer('False')]
        )
    q2 = RadioField(
        "True or False: You do not need a spotter to help back your truck up.",
        choices=[('True'), ('False')],
        validators=[CorrectAnswer('False')]
        )
    q3 = RadioField(
        "After putting the trailer on the ball of the hitch, what should be done next?",
        choices=[('Attach the chains'), ('Insert cotter pin through trailer lock'), ('Drive away'), ('Insert electrical plug')],
        validators=[CorrectAnswer('Insert cotter pin through trailer lock')]
        )
    q4 = RadioField(
        "When the chains are attached to the truck from the trailer, in what manner should they be done?",
        choices=[('Chains crossed once'), ('Chains not crossed'), ('Chains should not be attached'), ('Chains crossed ten times')],
        validators=[CorrectAnswer('Chains crossed once')]
        )
    q5 = RadioField(
        "True or False: A trailer breakaway cable is not on every trailer.",
        choices=[('True'), ('False')],
        validators=[CorrectAnswer('True')]
        )