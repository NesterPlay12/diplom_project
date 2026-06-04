from datetime import datetime, timedelta
import random
from app import create_app
from app.models import db, User, Category, Product, Review

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.count() > 0:
        print("База уже заполнена, запускаем только отзывы...")
        users_exist = True
    else:
        users_exist = False

    if not users_exist:
        admin = User(username='admin', email='admin@wildmarket.ru', role='admin', phone='+7-800-555-00-00', is_active=True)
        admin.set_password('admin123')
        db.session.add(admin)

        moderator = User(username='moderator', email='moder@wildmarket.ru', role='moderator', is_active=True)
        moderator.set_password('moder123')
        db.session.add(moderator)

        seller1 = User(username='seller_tech', email='seller1@wildmarket.ru', role='seller', is_active=True)
        seller1.set_password('seller123')
        db.session.add(seller1)

        seller2 = User(username='seller_fashion', email='seller2@wildmarket.ru', role='seller', is_active=True)
        seller2.set_password('seller123')
        db.session.add(seller2)

        buyer = User(username='ivan_petrov', email='ivan@example.ru', role='user', phone='+7-999-123-45-67', is_active=True)
        buyer.set_password('user123')
        db.session.add(buyer)

        db.session.flush()

        cats_data = [
            ('Электроника', 'electronics', '💻', None),
            ('Одежда', 'clothing', '👗', None),
            ('Обувь', 'shoes', '👟', None),
            ('Красота', 'beauty', '💄', None),
            ('Дом и сад', 'home', '🏠', None),
            ('Спорт', 'sport', '⚽', None),
            ('Детское', 'kids', '🧸', None),
            ('Книги', 'books', '📚', None),
        ]

        cats = {}
        for name, slug, icon, parent in cats_data:
            c = Category(name=name, slug=slug, icon=icon)
            db.session.add(c)
            cats[slug] = c

        db.session.flush()

        sub_cats = [
            ('Смартфоны', 'smartphones', '📱', 'electronics'),
            ('Ноутбуки', 'laptops', '💻', 'electronics'),
            ('Наушники', 'headphones', '🎧', 'electronics'),
            ('Мужская одежда', 'mens-clothing', '👔', 'clothing'),
            ('Женская одежда', 'womens-clothing', '👗', 'clothing'),
        ]

        for name, slug, icon, parent_slug in sub_cats:
            c = Category(name=name, slug=slug, icon=icon, parent_id=cats[parent_slug].id)
            db.session.add(c)
            cats[slug] = c

        db.session.flush()

        seller1_id = seller1.id
        seller2_id = seller2.id

        products_data = [
            ('iPhone 15 Pro 256GB', 'Флагманский смартфон Apple с процессором A17 Pro, камерой 48 Мп и USB-C. Цвет: титан. Дисплей 6.1"', 119990, 149990, 'Apple', 'smartphones', seller1_id, 50, 'https://images.unsplash.com/photo-1663499482523-1c0c1bae4ce1?w=400'),
            ('Samsung Galaxy S24 Ultra', 'Флагман Samsung с S Pen, камерой 200 Мп и AI-функциями. 12GB RAM, 256GB.', 109990, 129990, 'Samsung', 'smartphones', seller1_id, 30, 'https://images.unsplash.com/photo-1610945264803-c22b62d2a7b3?w=400'),
            ('MacBook Air M3 13"', 'Ноутбук Apple с чипом M3, 8GB RAM, 256GB SSD, 18 часов работы без зарядки.', 119990, 139990, 'Apple', 'laptops', seller1_id, 20, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400'),
            ('Sony WH-1000XM5', 'Беспроводные наушники с лучшим в классе шумоподавлением, 30 часов работы.', 29990, 39990, 'Sony', 'headphones', seller1_id, 45, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'),
            ('Xiaomi Redmi Note 13 Pro', 'Смартфон с камерой 200 Мп, AMOLED 120 Гц, 5000 мАч, быстрая зарядка 67W.', 24990, 29990, 'Xiaomi', 'smartphones', seller1_id, 80, 'https://images.unsplash.com/photo-1598327106026-d9521da673d1?w=400'),
            ('Платье летнее миди', 'Лёгкое платье из 100% хлопка с цветочным принтом. Размеры 42-52.', 2990, 4990, 'FashionLine', 'womens-clothing', seller2_id, 120, 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400'),
            ('Джинсы прямые мужские', 'Классические прямые джинсы из денима 320г/м². Размеры 28-38.', 3490, 5990, 'DenimCo', 'mens-clothing', seller2_id, 90, 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'),
            ('Кроссовки беговые', 'Лёгкие беговые кроссовки с амортизацией EVA. Размеры 36-46.', 6990, 9990, 'RunMax', 'shoes', seller2_id, 60, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'),
            ('Набор для ухода за лицом', 'Комплекс из 5 средств: тоник, сыворотка, крем, маска, мицеллярная вода.', 3990, 6990, 'BeautyRus', 'beauty', seller2_id, 200, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'),
            ('Фитнес-браслет Mi Band 8', 'Умный браслет с AMOLED-экраном, 150+ режимов тренировок, SpO2, 16 дней работы.', 4990, 6990, 'Xiaomi', 'sport', seller1_id, 150, 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400'),
            ('Конструктор LEGO City', 'Набор LEGO "Полицейский участок", 668 деталей, для детей от 6 лет.', 5990, 7990, 'LEGO', 'kids', seller2_id, 40, 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400'),
            ('Гарри Поттер: Полное собрание', 'Все 7 книг серии о Гарри Поттере в твёрдом переплёте. Перевод Mahon.', 4490, 5990, 'Азбука', 'books', seller2_id, 75, 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400'),
        ]

        products = []
        for name, desc, price, old_price, brand, cat_slug, seller_id, stock, img in products_data:
            p = Product(
                name=name, description=desc, price=price, old_price=old_price,
                brand=brand, category_id=cats[cat_slug].id, seller_id=seller_id,
                stock=stock, rating=0.0, review_count=0,
                image_url=img, is_active=True, is_approved=True
            )
            db.session.add(p)
            products.append(p)

        db.session.flush()
    else:
        products = Product.query.filter_by(is_active=True, is_approved=True).all()

    # Создаём реальных пользователей-покупателей для отзывов
    reviewer_data = [
        ('aleksey_k', 'aleksey@mail.ru'),
        ('marina_s', 'marina@gmail.com'),
        ('dmitry_v', 'dmitry@yandex.ru'),
        ('olga_m', 'olga@mail.ru'),
        ('sergey_p', 'sergey@gmail.com'),
        ('natasha_r', 'natasha@yandex.ru'),
        ('andrey_l', 'andrey@mail.ru'),
        ('ekaterina_b', 'ekaterina@gmail.com'),
        ('nikolay_t', 'nikolay@yandex.ru'),
        ('tatyana_f', 'tatyana@mail.ru'),
        ('mikhail_z', 'mikhail@gmail.com'),
        ('anna_g', 'anna@yandex.ru'),
    ]

    reviewers = []
    for uname, email in reviewer_data:
        existing = User.query.filter_by(email=email).first()
        if existing:
            reviewers.append(existing)
        else:
            u = User(username=uname, email=email, role='user', is_active=True)
            u.set_password('user123')
            db.session.add(u)
            reviewers.append(u)

    db.session.flush()

    # Реальные тексты отзывов для каждого товара
    reviews_data = {
        'iPhone 15 Pro 256GB': [
            (5, 'aleksey_k', 'Отличный телефон! Камера просто фантастическая, снимки получаются чёткими даже ночью. USB-C — наконец-то! Батарея держит весь день при активном использовании. Очень доволен покупкой.'),
            (5, 'marina_s', 'Пользуюсь уже 3 месяца — полный восторг. Dynamic Island удобнее, чем казалось поначалу. Titanium корпус не скользит в руке. Рекомендую всем, кто думает.'),
            (4, 'dmitry_v', 'Телефон хорош, но цена кусается. За эти деньги ожидал чуть более мощную батарею. В остальном — безупречно: скорость, дисплей, камера. Переехал с S22 и не жалею.'),
            (5, 'olga_m', 'Брала в подарок мужу — он в восторге! Говорит, что это лучший телефон, что у него был. Игры летают, фото невероятные. Доставка пришла быстро, упаковка целая.'),
            (4, 'sergey_p', 'Хороший аппарат. Единственный минус — нагревается при долгой съёмке видео. Но в целом производительность на высоте, дисплей яркий, Face ID работает мгновенно.'),
        ],
        'Samsung Galaxy S24 Ultra': [
            (5, 'natasha_r', 'S Pen изменил мою жизнь! Делаю заметки прямо на экране, рисую скетчи. Камера 200 Мп — это что-то невероятное. Зум 100x реально работает. Топовый телефон!'),
            (4, 'andrey_l', 'Мощный зверь. AI-функции реально полезны — Circle to Search экономит кучу времени. Минус — телефон тяжёлый и большой, не для маленьких рук. В остальном — шедевр.'),
            (5, 'ekaterina_b', 'Перешла с iPhone и не жалею. Кастомизация Android — это свобода. Экран яркий даже на солнце. Батарея держит 1,5 дня. Очень довольна!'),
            (3, 'nikolay_t', 'Телефон хороший, но OneUI перегружен лишними приложениями. Пришлось потратить время на настройку. После чистки — летает. Камера супер.'),
        ],
        'MacBook Air M3 13"': [
            (5, 'tatyana_f', 'Работаю дизайнером — это идеальный ноут для моих задач. Процессор M3 справляется со всем: Figma, Photoshop, видео. Без вентилятора — тишина! Заряда хватает на рабочий день.'),
            (5, 'mikhail_z', 'Купил для работы и учёбы. Лёгкий как перо, экран отличный, клавиатура удобная. Через месяц использования — ни одного нарекания. MacOS — это просто удовольствие.'),
            (5, 'anna_g', 'Пересела с Windows — разница колоссальная. Всё работает мгновенно, ничего не зависает. 18 часов батареи — это правда. Рекомендую без сомнений.'),
            (4, 'aleksey_k', 'Отличная машина. Единственное — хотелось бы больше RAM в базовой версии (8 GB маловато для тяжёлых задач). Брал 16 GB — проблем нет.'),
        ],
        'Sony WH-1000XM5': [
            (5, 'marina_s', 'Лучшие наушники, что у меня были! Шумоподавление — как вата в ушах, весь мир исчезает. На работе в открытом офисе — спасение. Звук тёплый, детальный. 30 часов — реальная цифра.'),
            (5, 'dmitry_v', 'Использую в метро каждый день. Шумоподавление фантастическое. LDAC-кодек даёт отличное качество с Android. Очень лёгкие, не устают уши после 4 часов. Однозначно топ.'),
            (4, 'olga_m', 'Звук прекрасный, шумодав работает. Единственный минус — сенсорная панель иногда срабатывает случайно в кармане. Но в целом покупкой очень довольна.'),
            (5, 'sergey_p', 'Для работы из дома это находка. Созвоны кристально чистые, музыка — огонь. Складываются компактно, удобно брать в дорогу. Стоит каждого рубля!'),
            (5, 'natasha_r', 'Подарила мужу — он теперь не снимает. Говорит, что слышит в музыке детали, которые раньше не замечал. Упаковка роскошная, всё есть в комплекте.'),
        ],
        'Xiaomi Redmi Note 13 Pro': [
            (5, 'andrey_l', 'За такие деньги — просто бомба! Камера 200 Мп делает снимки не хуже флагмана. AMOLED-дисплей яркий, 120 Гц — всё плавно. Быстрая зарядка 67W заряжает за час.'),
            (4, 'ekaterina_b', 'Хороший середнячок. Производительности хватает для всего: игры, соцсети, работа. Камера днём отличная, ночью — неплохо. Батарея 5000 мАч тянет 2 дня.'),
            (4, 'nikolay_t', 'Брал как второй телефон — доволен. Лёгкий, красивый, шустрый. MIUI немного раздражает рекламой, но отключается. Рекомендую за свои деньги.'),
            (3, 'tatyana_f', 'Телефон неплохой, но нагревается при игре в Genshin Impact. В остальном всё нормально. Камера хороша для соцсетей.'),
        ],
        'Платье летнее миди': [
            (5, 'mikhail_z', 'Купил жене — она в восторге! Ткань приятная к телу, не мнётся. Размер соответствует. Цвет насыщенный, как на фото. Придём ещё.'),
            (5, 'anna_g', 'Заказала для отпуска — лучший выбор! Хлопок дышащий, в жару очень комфортно. Крой универсальный, подходит и на пляж, и на прогулку. Беру в следующий раз ещё один цвет.'),
            (4, 'aleksey_k', 'Платье красивое, качество хорошее. Длина чуть дольше, чем казалось по фото, но это даже лучше. Доставка быстрая.'),
        ],
        'Джинсы прямые мужские': [
            (5, 'marina_s', 'Брала мужу — сидят идеально! Плотная ткань, хорошо держит форму. Размерная сетка точная. Уже носит третий месяц — не вытягиваются, цвет не выгорает.'),
            (4, 'dmitry_v', 'Добротные джинсы. Посадка классическая, как раньше делали. Пришлось немного ушить в талии, но это мой типаж. Качество на 4+.'),
            (5, 'olga_m', 'Отличные джинсы! Муж носит постоянно. Говорит, очень удобные и не сковывают движения. Рекомендую!'),
        ],
        'Кроссовки беговые': [
            (5, 'sergey_p', 'Бегаю в них уже 4 месяца — нога не устаёт даже на 15 км. Амортизация отличная, сетка дышащая. После стирки как новые. Отличная покупка для любителей бега.'),
            (4, 'natasha_r', 'Лёгкие и удобные. Для утренних пробежек самое то. Единственное — подошва немного скользит на мокром асфальте. В остальном без нареканий.'),
            (5, 'andrey_l', 'Брал для зала — доволен. Хорошая фиксация голеностопа, не натирают. Размер точно по сетке. Рекомендую!'),
            (4, 'ekaterina_b', 'Симпатичные и лёгкие. Для прогулок и лёгкого бега подходят отлично. На марафон бы взял что-то серьёзнее, а для любителей — в самый раз.'),
        ],
        'Набор для ухода за лицом': [
            (5, 'nikolay_t', 'Купил жене — говорит, что кожа стала заметно лучше уже через 2 недели. Набор полный: утро и вечер закрыты. Тоник не щиплет, крем не жирнит. Однозначно берём ещё.'),
            (5, 'tatyana_f', 'Пользуюсь месяц — результат виден! Поры уменьшились, кожа увлажнённая весь день. Сыворотка особенно понравилась. Натуральный состав, никаких раздражений.'),
            (4, 'mikhail_z', 'Хороший набор за свои деньги. Запах нейтральный, не аллергенный. Тюбики большие — хватит надолго. Рекомендую как подарок.'),
            (5, 'anna_g', 'Уже второй раз заказываю! Первый набор закончился за 3 месяца. Кожа реально стала лучше. Маска — отдельный восторг, снимаю усталость за 15 минут.'),
        ],
        'Фитнес-браслет Mi Band 8': [
            (5, 'aleksey_k', 'Слежу за сном, шагами и пульсом. Всё точно работает. SpO2 показывает стабильно. AMOLED-экран чёткий даже на солнце. 16 дней батарея — это реальность.'),
            (5, 'marina_s', 'Отличный браслет! Стильный, лёгкий, незаметен на руке. Уведомления приходят вовремя, вибрация ощутимая. Рекомендую всем, кто хочет следить за здоровьем.'),
            (4, 'dmitry_v', 'Хороший трекер за небольшие деньги. GPS нет (только через телефон), но для ходьбы и бега хватает. Измерение стресса немного сомнительное, но остальные функции работают.'),
            (4, 'olga_m', 'Красивый и удобный. Ремешок мягкий, не потеет под ним. Приложение Mi Fitness понятное. Единственное — хотелось бы оплату через NFC.'),
        ],
        'Конструктор LEGO City': [
            (5, 'sergey_p', 'Сыну 8 лет — в восторге! Собирали вместе три вечера. Детали все на месте, инструкция понятная. Полицейский участок получился большой и детальный. Хранится теперь на почётном месте.'),
            (5, 'natasha_r', 'Купила племяннику на день рождения. Мама написала, что не могли оторваться! Качество LEGO всегда на высоте. Доставка быстрая, коробка целая.'),
            (5, 'andrey_l', 'LEGO никогда не подводит. Дочке 7 лет — справилась сама почти без помощи. Фигурки крутые, есть машины и аксессуары. Рекомендую!'),
            (4, 'ekaterina_b', 'Набор отличный, но мелкие детали теряются быстро. Советую сразу купить сортировочный поднос. В остальном — качество как всегда превосходное.'),
        ],
        'Гарри Поттер: Полное собрание': [
            (5, 'nikolay_t', 'Покупал для дочери 10 лет — теперь не оторвать! Качество книг отличное: плотная бумага, твёрдый переплёт, иллюстрации. Перевод хороший, читается легко. Отличный подарок!'),
            (5, 'tatyana_f', 'Наконец собрала всю серию! Книги выглядят роскошно на полке. Дочитала сама за месяц — не могла остановиться. Для детей и взрослых одинаково хороши.'),
            (5, 'mikhail_z', 'Брал себе — читал в детстве только пиратские издания, захотел нормальные. Бумага приятная, не просвечивает. Шрифт удобный. Уже третья перечитка — и всё равно захватывает!'),
            (5, 'anna_g', 'Подарила сестре на Новый год — она была в слезах от радости! Упаковка на сайте была аккуратной, книги пришли в идеальном состоянии. Однозначно лучший подарок.'),
            (5, 'aleksey_k', 'Классика. Сыну 12 лет — прочитал все 7 книг за 2 месяца. Раньше вообще не любил читать. Теперь просит следующую серию. Магия работает!'),
        ],
    }

    # Удаляем существующие отзывы если запускаем повторно
    if users_exist:
        existing_review_count = Review.query.count()
        if existing_review_count > 0:
            print(f"Удаляем {existing_review_count} существующих отзывов...")
            Review.query.delete()
            db.session.flush()

    review_count = 0
    for product in products:
        if product.name not in reviews_data:
            continue

        product_reviews = reviews_data[product.name]
        all_ratings = []

        for rating, reviewer_username, text in product_reviews:
            reviewer = User.query.filter_by(username=reviewer_username).first()
            if not reviewer:
                continue

            existing = Review.query.filter_by(user_id=reviewer.id, product_id=product.id).first()
            if existing:
                continue

            days_ago = random.randint(1, 180)
            created_at = datetime.utcnow() - timedelta(days=days_ago)

            review = Review(
                user_id=reviewer.id,
                product_id=product.id,
                rating=rating,
                text=text,
                created_at=created_at
            )
            db.session.add(review)
            all_ratings.append(rating)
            review_count += 1

        if all_ratings:
            product.rating = round(sum(all_ratings) / len(all_ratings), 1)
            product.review_count = len(all_ratings)

    db.session.commit()
    print("✅ База данных заполнена:")
    print(f"   Пользователи: {User.query.count()}")
    print(f"   Категории: {Category.query.count()}")
    print(f"   Товары: {Product.query.count()}")
    print(f"   Отзывы: {Review.query.count()}")
    print()
    print("Тестовые аккаунты:")
    print("  Админ:      admin@wildmarket.ru / admin123")
    print("  Продавец:   seller1@wildmarket.ru / seller123")
    print("  Покупатель: ivan@example.ru / user123")
