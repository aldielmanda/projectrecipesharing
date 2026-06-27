from app import create_app
from app.extensions import db
from app.models import User, FoodRecipe, DrinkRecipe, Ingredient, Review

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    admin = User(username="admin", email="admin@gmail.com", role="admin")
    admin.password = "admin123"

    deni = User(username="deni_andika", email="deni@gmail.com", role="user")
    deni.password = "deni123"

    aldi = User(username="aldi_elmanda", email="aldi@gmail.com", role="user")
    aldi.password = "aldi123"

    db.session.add_all([admin, deni, aldi])
    db.session.commit()

    # Resep Makanan
    r1 = FoodRecipe(
        title="Mie Aceh Kepiting Spesial",
        category="main course",
        steps="1. Tumis bumbu Aceh hingga harum\n2. Masukkan kepiting & tuang kaldu\n3. Masukkan mie kuning, masak hingga bumbu meresap\n4. Sajikan dengan acar dan emping",
        cooking_time=25,
        author=deni
    )

    r2 = FoodRecipe(
        title="Nasi Goreng Kampung",
        category="main course",
        steps="1. Panaskan minyak, tumis bawang merah & putih\n2. Masukkan cabai, aduk rata\n3. Tambahkan nasi, kecap manis & garam\n4. Masukkan telur, orak-arik hingga matang\n5. Sajikan dengan kerupuk & acar",
        cooking_time=15,
        author=deni
    )

    r3 = FoodRecipe(
        title="Ayam Geprek Sambal Bawang",
        category="main course",
        steps="1. Marinasi ayam dengan bumbu selama 30 menit\n2. Goreng ayam hingga crispy kecoklatan\n3. Ulek cabai rawit & bawang putih kasar\n4. Geprek ayam di atas sambal\n5. Sajikan dengan nasi & lalapan",
        cooking_time=45,
        author=aldi
    )

    r4 = FoodRecipe(
        title="Pisang Goreng Crispy Coklat",
        category="dessert",
        steps="1. Kupas pisang, belah jadi 2\n2. Buat adonan tepung dengan air es & gula\n3. Celupkan pisang ke adonan\n4. Goreng hingga keemasan & renyah\n5. Taburi coklat leleh & keju parut",
        cooking_time=20,
        author=aldi
    )

    r5 = FoodRecipe(
        title="Lumpia Sayur Goreng",
        category="appetizer",
        steps="1. Tumis wortel, kol & tauge dengan bumbu\n2. Tambahkan soun yang sudah direndam\n3. Bungkus isian dengan kulit lumpia\n4. Goreng dalam minyak panas hingga kecoklatan\n5. Sajikan dengan saus sambal",
        cooking_time=30,
        author=admin
    )

    r6 = FoodRecipe(
        title="Bubur Sumsum Gula Merah",
        category="dessert",
        steps="1. Larutkan tepung beras dengan santan & garam\n2. Masak sambil diaduk hingga mengental\n3. Masak gula merah & daun pandan jadi saus\n4. Sajikan bubur dengan siraman saus gula merah",
        cooking_time=25,
        author=admin
    )

    # Resep Minuman
    r7 = DrinkRecipe(
        title="Es Timun Serut Selasih",
        category="appetizer",
        steps="1. Serut timun secara memanjang\n2. Campur dengan sirup melon dan selasih yang sudah direndam\n3. Tuang air dan aduk rata\n4. Beri es batu secukupnya\n5. Sajikan dingin",
        is_cold_served=True,
        author=deni
    )

    r8 = DrinkRecipe(
        title="Es Teh Susu Boba",
        category="appetizer",
        steps="1. Seduh teh hitam pekat, biarkan dingin\n2. Masak boba hingga kenyal, rendam di air gula\n3. Campurkan teh, susu kental manis & es batu\n4. Masukkan boba ke gelas\n5. Tuang campuran teh susu di atasnya",
        is_cold_served=True,
        author=aldi
    )

    r9 = DrinkRecipe(
        title="Wedang Jahe Rempah",
        category="appetizer",
        steps="1. Geprek jahe, kayu manis & cengkeh\n2. Rebus semua rempah dengan air 10 menit\n3. Tambahkan gula merah & daun pandan\n4. Saring dan tuang ke gelas\n5. Sajikan hangat",
        is_cold_served=False,
        author=aldi
    )

    r10 = DrinkRecipe(
        title="Jus Alpukat Susu",
        category="appetizer",
        steps="1. Belah alpukat matang, ambil dagingnya\n2. Masukkan ke blender bersama susu UHT & es batu\n3. Tambahkan gula pasir & sedikit garam\n4. Blender hingga lembut & creamy\n5. Tuang ke gelas, beri topping coklat",
        is_cold_served=True,
        author=admin
    )

    db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10])
    db.session.commit()

    # Ingredients
    db.session.add_all([
        # r1 - Mie Aceh
        Ingredient(name="Mie Kuning Basah",   amount="500 gram",   recipe_id=r1.id),
        Ingredient(name="Kepiting Segar",      amount="2 ekor",     recipe_id=r1.id),
        Ingredient(name="Bumbu Aceh",          amount="3 sdm",      recipe_id=r1.id),
        Ingredient(name="Kaldu Seafood",       amount="500 ml",     recipe_id=r1.id),

        # r2 - Nasi Goreng
        Ingredient(name="Nasi Putih",          amount="2 piring",   recipe_id=r2.id),
        Ingredient(name="Telur Ayam",          amount="2 butir",    recipe_id=r2.id),
        Ingredient(name="Kecap Manis",         amount="2 sdm",      recipe_id=r2.id),
        Ingredient(name="Bawang Merah",        amount="4 siung",    recipe_id=r2.id),
        Ingredient(name="Cabai Rawit",         amount="5 buah",     recipe_id=r2.id),

        # r3 - Ayam Geprek
        Ingredient(name="Ayam Potong",         amount="4 potong",   recipe_id=r3.id),
        Ingredient(name="Tepung Bumbu",        amount="200 gram",   recipe_id=r3.id),
        Ingredient(name="Cabai Rawit Merah",   amount="15 buah",    recipe_id=r3.id),
        Ingredient(name="Bawang Putih",        amount="5 siung",    recipe_id=r3.id),

        # r4 - Pisang Goreng
        Ingredient(name="Pisang Kepok",        amount="4 buah",     recipe_id=r4.id),
        Ingredient(name="Tepung Terigu",       amount="150 gram",   recipe_id=r4.id),
        Ingredient(name="Coklat Leleh",        amount="50 gram",    recipe_id=r4.id),
        Ingredient(name="Keju Parut",          amount="secukupnya", recipe_id=r4.id),

        # r5 - Lumpia
        Ingredient(name="Kulit Lumpia",        amount="15 lembar",  recipe_id=r5.id),
        Ingredient(name="Wortel",              amount="2 buah",     recipe_id=r5.id),
        Ingredient(name="Kol",                 amount="100 gram",   recipe_id=r5.id),
        Ingredient(name="Soun",                amount="50 gram",    recipe_id=r5.id),

        # r6 - Bubur Sumsum
        Ingredient(name="Tepung Beras",        amount="100 gram",   recipe_id=r6.id),
        Ingredient(name="Santan",              amount="400 ml",     recipe_id=r6.id),
        Ingredient(name="Gula Merah",          amount="150 gram",   recipe_id=r6.id),
        Ingredient(name="Daun Pandan",         amount="2 lembar",   recipe_id=r6.id),

        # r7 - Es Timun
        Ingredient(name="Timun",               amount="2 buah",     recipe_id=r7.id),
        Ingredient(name="Sirup Melon",         amount="3 sdm",      recipe_id=r7.id),
        Ingredient(name="Biji Selasih",        amount="1 sdt",      recipe_id=r7.id),
        Ingredient(name="Es Batu",             amount="secukupnya", recipe_id=r7.id),

        # r8 - Es Teh Boba
        Ingredient(name="Teh Hitam",           amount="2 kantong",  recipe_id=r8.id),
        Ingredient(name="Boba / Tapioka",      amount="100 gram",   recipe_id=r8.id),
        Ingredient(name="Susu Kental Manis",   amount="3 sdm",      recipe_id=r8.id),
        Ingredient(name="Es Batu",             amount="secukupnya", recipe_id=r8.id),

        # r9 - Wedang Jahe
        Ingredient(name="Jahe",                amount="3 ruas",     recipe_id=r9.id),
        Ingredient(name="Kayu Manis",          amount="1 batang",   recipe_id=r9.id),
        Ingredient(name="Gula Merah",          amount="100 gram",   recipe_id=r9.id),
        Ingredient(name="Cengkeh",             amount="3 butir",    recipe_id=r9.id),

        # r10 - Jus Alpukat
        Ingredient(name="Alpukat Matang",      amount="2 buah",     recipe_id=r10.id),
        Ingredient(name="Susu UHT Full Cream", amount="200 ml",     recipe_id=r10.id),
        Ingredient(name="Gula Pasir",          amount="2 sdm",      recipe_id=r10.id),
        Ingredient(name="Es Batu",             amount="secukupnya", recipe_id=r10.id),
    ])
    db.session.commit()

    # Reviews dummy
    db.session.add_all([
        Review(rating=5, comment="Enak banget! Bumbu Acehnya kerasa banget.", user_id=aldi.id,  recipe_id=r1.id),
        Review(rating=4, comment="Mantap, bumbunya pas!",                     user_id=admin.id, recipe_id=r2.id),
        Review(rating=5, comment="Gepreknya crispy, sambalnya nampol!",       user_id=deni.id,  recipe_id=r3.id),
        Review(rating=4, comment="Seger banget, cocok buat cuaca panas.",     user_id=admin.id, recipe_id=r7.id),
        Review(rating=5, comment="Bobanya kenyal, tehnya pas manisnya.",      user_id=deni.id,  recipe_id=r8.id),
    ])
    db.session.commit()

    # Sync rating semua resep yang punya review
    from app.models import Recipe
    for recipe in Recipe.query.all():
        recipe.sync_rating()
    db.session.commit()

    print("=" * 50)
    print("Berhasil! Database telah diisi dengan:")
    print(f"  - 3 user (admin, deni_andika, aldi_elmanda)")
    print(f"  - 6 resep makanan (FoodRecipe)")
    print(f"  - 4 resep minuman (DrinkRecipe)")
    print(f"  - 5 review dummy")
    print("=" * 50)