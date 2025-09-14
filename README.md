# Fregith Calculator Django

Aplikasi ini adalah kalkulator untuk menghitung biaya pengiriman barang menggunakan Django + Sqlite.

## Instalasi

1. Clone repositori:

```bash
git clone https://github.com/tiedsandi/fregith-calculator-django.git
cd fregith-calculator-django
```

2. Install dependencies:

```bash
pip install django djangorestframework requests django-cors-headers djangorestframework-simplejwt
```

3. Migrasi database:

```bash
python manage.py migrate
```

4. Load initial data:

```bash
python manage.py loaddata dashboard/fixtures/initial_data.json
```

5. Jalankan server:

```bash
python manage.py runserver
```

## Penggunaan

1. Buka browser dan akses `http://localhost:8000/`.
2. **Login terlebih dahulu**.
   - Jika belum punya akun, silakan **register** dulu.
3. Setelah login, akan diarahkan ke halaman `/` (dashboard).
   - Di dashboard, user bisa memilih menu **Country** atau **Category**.
   - User bisa **membuat, mengedit, atau menghapus** Country / Category yang sudah dibuat (CRUD).
4. User juga bisa melakukan **logout** dari dashboard.

---

### API Endpoints

| Endpoint           | Method | Query / Payload                                               | Keterangan                                                                                                                     |
| ------------------ | ------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `/api/countries`   | GET    | `search={query}`                                              | Cari country berdasarkan nama                                                                                                  |
| `/api/categories`  | GET    | `country_id={id}&search={query}`                              | Cari category di country tertentu (search opsional)                                                                            |
| `/api/destination` | GET    | `search={city}`                                               | Cari destination city                                                                                                          |
| `/api/calculate`   | POST   | JSON: `country_id`, `category_id`, `destination_id`, `weight` | Menghitung freight, response: `origin`, `destination`, `category_name`, `international_price`, `domestic_price`, `total_price` |
