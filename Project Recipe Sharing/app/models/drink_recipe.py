from app.extensions import db
from app.models.recipe import Recipe

class DrinkRecipe(Recipe):
    is_cold_served = db.Column(db.Boolean, default=True)
    __mapper_args__ = {'polymorphic_identity': 'drink'}
    def display_meta(self):
        s = "Dingin & Es ❄️" if self.is_cold_served else "Hangat/Panas ☕"
        return f"🥤 Minuman Olahan | Penyajian: {s}"