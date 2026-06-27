from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

class RecipeForm(FlaskForm):
    title = StringField('Nama Masakan / Minuman', validators=[DataRequired()])
    category = SelectField('Kategori Sajian', choices=[('appetizer', 'Appetizer'), ('main course', 'Main Course'), ('dessert', 'Dessert')])
    recipe_type = SelectField('Klasifikasi Resep (Prinsip OOP Polymorphic)', choices=[('food', 'Makanan Padat (FoodRecipe)'), ('drink', 'Minuman (DrinkRecipe)')])
    cooking_time = IntegerField('Durasi Masak (Menit - Khusus Makanan)', validators=[Optional()])
    is_cold_served = BooleanField('Sajikan dalam Kondisi Dingin (Khusus Minuman)')
    steps = TextAreaField('Tahapan Pembuatan', validators=[DataRequired()])
    submit = SubmitField('Publikasikan Resep')

class ReviewForm(FlaskForm):
    rating = SelectField('Nilai Bintang', choices=[(5, '⭐⭐⭐⭐⭐ (5)'), (4, '⭐⭐⭐⭐ (4)'), (3, '⭐⭐⭐ (3)'), (2, '⭐⭐ (2)'), (1, '⭐ (1)')], coerce=int)
    comment = TextAreaField('Komentar Opsional', validators=[Optional()])
    submit = SubmitField('Kirim Penilaian')