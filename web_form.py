import flask_wtf
import wtforms

from passport_mrz_td3_decoder import PASSPORT_MRZ_LINE_LENGTH

class SubmitPassportMRZForm(flask_wtf.FlaskForm):

    mrz_line_1 = wtforms.StringField("mrz_line_1", validators=[wtforms.validators.Length(min=PASSPORT_MRZ_LINE_LENGTH-1, max=PASSPORT_MRZ_LINE_LENGTH+1)])
    mrz_line_2 = wtforms.StringField("mrz_line_2", validators=[wtforms.validators.Length(min=PASSPORT_MRZ_LINE_LENGTH-1, max=PASSPORT_MRZ_LINE_LENGTH+1)])

    passport_img_file = flask_wtf.FileField()

    submit = wtforms.SubmitField("Submit")