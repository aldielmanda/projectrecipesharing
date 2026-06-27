import unittest
from app import create_app
from app.extensions import db
from app.models import User, FoodRecipe

class OOPTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.ctx = self.app.app_context(); self.ctx.push()
        db.create_all()
    def tearDown(self): db.session.remove(); db.drop_all(); self.ctx.pop()
    
    def test_encapsulation(self):
        u = User(username="t", email="t@t.com"); u.password="secret"
        self.assertTrue(u.verify_password("secret"))
        with self.assertRaises(AttributeError): _ = u.password
        
    def test_polymorphic_display(self):
        u = User(username="c", email="c@c.com"); u.password="1"; db.session.add(u); db.session.commit()
        fr = FoodRecipe(title="Sate", category="main course", steps="bakar", cooking_time=15, author=u)
        db.session.add(fr); db.session.commit()
        self.assertIn("15 Menit", fr.display_meta())

if __name__ == '__main__': unittest.main()