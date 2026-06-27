from app.extensions import db
from app.models.recipe import Recipe

class FoodRecipe(Recipe):
    cooking_time = db.Column(db.Integer, nullable=True)
    __mapper_args__ = {'polymorphic_identity': 'food'}
    def display_meta(self): return f"🍽️ Makanan Utama | Waktu Masak: {self.cooking_time or 0} Menit"