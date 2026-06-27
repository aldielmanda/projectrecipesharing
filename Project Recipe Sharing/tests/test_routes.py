import unittest
from app import create_app
from app.extensions import db
from app.models import User, FoodRecipe, DrinkRecipe, Ingredient, Bookmark, Review


class RoutesTestCase(unittest.TestCase):
    """Test case untuk memverifikasi semua route utama aplikasi."""

    def setUp(self):
        """Inisialisasi app testing dengan database in-memory."""
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Nonaktifkan CSRF saat testing
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

        # Buat user dummy untuk testing
        self.user = User(username='testuser', email='test@test.com', role='user')
        self.user.password = 'password123'
        self.admin = User(username='adminuser', email='admin@test.com', role='admin')
        self.admin.password = 'admin123'
        db.session.add_all([self.user, self.admin])
        db.session.commit()

        # Buat resep dummy
        self.food = FoodRecipe(
            title='Nasi Goreng',
            category='main course',
            steps='1. Goreng nasi\n2. Tambah kecap',
            cooking_time=10,
            author=self.user
        )
        self.drink = DrinkRecipe(
            title='Es Teh Manis',
            category='appetizer',
            steps='1. Seduh teh\n2. Tambah gula\n3. Beri es',
            is_cold_served=True,
            author=self.user
        )
        db.session.add_all([self.food, self.drink])
        db.session.commit()

    def tearDown(self):
        """Bersihkan database setelah setiap test."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login(self, username='testuser', password='password123'):
        """Helper method untuk login."""
        return self.client.post('/auth/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        """Helper method untuk logout."""
        return self.client.get('/auth/logout', follow_redirects=True)

    # ── Auth Routes ────────────────────────────────────────────────

    def test_halaman_login_dapat_diakses(self):
        """GET /auth/login harus mengembalikan status 200."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_halaman_register_dapat_diakses(self):
        """GET /auth/register harus mengembalikan status 200."""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)

    def test_login_berhasil_dengan_kredensial_valid(self):
        """Login dengan username & password benar harus redirect ke halaman utama."""
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Katalog', response.data)

    def test_login_gagal_dengan_password_salah(self):
        """Login dengan password salah harus menampilkan pesan error."""
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'passwordsalah'
        }, follow_redirects=True)
        self.assertIn('keliru'.encode(), response.data)

    def test_logout_berhasil(self):
        """Logout setelah login harus redirect ke halaman utama."""
        self.login()
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    # ── Recipe Routes ──────────────────────────────────────────────

    def test_halaman_index_dapat_diakses_tanpa_login(self):
        """GET / harus bisa diakses tanpa login (publik)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_halaman_index_menampilkan_resep(self):
        """Halaman index harus menampilkan judul resep yang ada."""
        response = self.client.get('/')
        self.assertIn(b'Nasi Goreng', response.data)
        self.assertIn(b'Es Teh Manis', response.data)

    def test_filter_kategori_berfungsi(self):
        """Filter category via query param harus memfilter resep dengan benar."""
        response = self.client.get('/?category=main+course')
        self.assertIn(b'Nasi Goreng', response.data)
        self.assertNotIn(b'Es Teh Manis', response.data)

    def test_halaman_detail_resep_dapat_diakses(self):
        """GET /<id> harus menampilkan detail resep."""
        response = self.client.get(f'/{self.food.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nasi Goreng', response.data)

    def test_detail_resep_tidak_ada_return_404(self):
        """GET dengan ID resep yang tidak ada harus return 404."""
        response = self.client.get('/9999')
        self.assertEqual(response.status_code, 404)

    def test_halaman_create_redirect_jika_belum_login(self):
        """GET /create tanpa login harus redirect ke halaman login."""
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.headers['Location'])

    def test_halaman_create_dapat_diakses_setelah_login(self):
        """GET /create setelah login harus return 200."""
        self.login()
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)

    def test_create_food_recipe_berhasil(self):
        """POST /create dengan data FoodRecipe valid harus berhasil membuat resep baru."""
        self.login()
        response = self.client.post('/create', data={
            'title': 'Soto Ayam',
            'category': 'main course',
            'recipe_type': 'food',
            'cooking_time': 30,
            'steps': '1. Rebus ayam\n2. Tambah bumbu',
            'ing_name': ['Ayam'],
            'ing_amount': ['1 ekor']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Soto Ayam', response.data)

    def test_delete_resep_oleh_pemilik_berhasil(self):
        """POST /<id>/delete oleh pemilik resep harus berhasil menghapus."""
        self.login()
        response = self.client.post(f'/{self.food.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        deleted = Recipe.query.get(self.food.id)
        self.assertIsNone(deleted)

    def test_delete_resep_oleh_user_lain_ditolak(self):
        """POST /<id>/delete oleh user yang bukan pemilik harus return 403."""
        # Login sebagai user lain
        other = User(username='other', email='other@test.com', role='user')
        other.password = 'other123'
        db.session.add(other)
        db.session.commit()
        self.client.post('/auth/login', data={'username': 'other', 'password': 'other123'})
        response = self.client.post(f'/{self.food.id}/delete')
        self.assertEqual(response.status_code, 403)

    # ── Bookmark Routes ────────────────────────────────────────────

    def test_halaman_bookmark_redirect_jika_belum_login(self):
        """GET /bookmarks/ tanpa login harus redirect ke login."""
        response = self.client.get('/bookmarks/')
        self.assertEqual(response.status_code, 302)

    def test_toggle_bookmark_tambah_dan_hapus(self):
        """POST /bookmarks/toggle/<id> harus menambah lalu menghapus bookmark."""
        self.login()
        # Tambah bookmark
        self.client.post(f'/bookmarks/toggle/{self.food.id}', follow_redirects=True)
        bm = Bookmark.query.filter_by(user_id=self.user.id, recipe_id=self.food.id).first()
        self.assertIsNotNone(bm)

        # Hapus bookmark (toggle lagi)
        self.client.post(f'/bookmarks/toggle/{self.food.id}', follow_redirects=True)
        bm = Bookmark.query.filter_by(user_id=self.user.id, recipe_id=self.food.id).first()
        self.assertIsNone(bm)

    def test_halaman_bookmark_menampilkan_resep_tersimpan(self):
        """Halaman bookmark harus menampilkan resep yang sudah di-bookmark."""
        self.login()
        self.client.post(f'/bookmarks/toggle/{self.drink.id}', follow_redirects=True)
        response = self.client.get('/bookmarks/')
        self.assertIn(b'Es Teh Manis', response.data)


# Import Recipe di level modul agar bisa dipakai di dalam test
from app.models import Recipe

if __name__ == '__main__':
    unittest.main()