# MovieApp

MovieApp, Django framework kullanılarak geliştirilmiş bir film listeleme ve detaylandırma uygulamasıdır.

## Kurulum

### Gereksinimler

- Python 3.8+
- Django 3.2.7+

### Adımlar

1. Depoyu klonlayın:

    ```sh
    git clone <repository-url>
    cd movieapp
    ```

2. Sanal ortam oluşturun ve etkinleştirin:

    ```sh
    python -m venv env
    source env/bin/activate  # MacOS/Linux
    .\env\Scripts\activate  # Windows
    ```

3. Gerekli paketleri yükleyin:

    ```sh
    pip install -r requirements.txt
    ```

4. Veritabanı migrasyonlarını uygulayın:

    ```sh
    python manage.py migrate
    ```

5. Geliştirme sunucusunu başlatın:

    ```sh
    python manage.py runserver
    ```

6. Tarayıcınızda `http://127.0.0.1:8000/` adresine gidin.

## Proje Yapısı

```plaintext
movieapp/
    ├── movieapp/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── __pycache__/
    ├── movies/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── __pycache__/
    │   ├── migrations/
    │   ├── static/
    │   └── templates/
    ├── static/
    │   ├── css/
    │   ├── img/
    │   ├── js/
    │   └── vendor/
    ├── templates/
    │   └── movies/
    ├── .gitignore
    ├── db.sqlite3
    └── manage.py
```

## Özellikler

- Film listeleme sayfası
- Film detay sayfası
- Dinamik veri gösterimi
- Slider bileşeni

## Ayarlar

Proje ayarları `movieapp/settings.py` dosyasında bulunmaktadır. Önemli ayarlar:

- `INSTALLED_APPS`: Uygulamalar ve Django bileşenleri
- `MIDDLEWARE`: Orta katman yazılımları
- `DATABASES`: Veritabanı ayarları (SQLite kullanılıyor)
- `STATIC_URL` ve `STATICFILES_DIRS`: Statik dosya ayarları