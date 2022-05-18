from flask_wtf import FlaskForm
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from wtforms import StringField, SubmitField, DecimalField, URLField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    name = StringField('Item Name', validators= [DataRequired()])
    desc = StringField('Description', validators= [DataRequired()])
    price = DecimalField('Price', validators= [DataRequired()])
    img = URLField('Image URL', validators= [DataRequired()])
    submit = SubmitField('Post')

class AddToCart(FlaskForm):
    submit = SubmitField('Add To Cart')

