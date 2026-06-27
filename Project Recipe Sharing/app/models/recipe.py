from app.extensions import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    steps = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    _total_score = db.Column('total_score', db.Integer, default=0)
    _review_count = db.Column('review_count', db.Integer, default=0)

    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan', lazy=True)
    reviews = db.relationship('Review', backref='recipe', cascade='all, delete-orphan', lazy=True)
    bookmarked_by = db.relationship('Bookmark', backref='recipe', cascade='all, delete-orphan', lazy=True)

    __mapper_args__ = {'polymorphic_on': type, 'polymorphic_identity': 'generic'}

    def get_average_rating(self):
        if self._review_count == 0: return 0.0
        return round(self._total_score / self._review_count, 1)

    def sync_rating(self):
        self._review_count = len(self.reviews)
        self._total_score = sum(r.rating for r in self.reviews)

    def display_meta(self): return "Resep Kuliner Dasar"