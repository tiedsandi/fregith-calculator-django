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

## Alur penggunaan aplikasi

1. **Dashboard (Monolith / Django Template)**

   - Buka browser dan akses `http://localhost:8000/`.
   - **Login terlebih dahulu** (jika belum punya akun, silakan register).
   - Setelah login, akan diarahkan ke halaman `/` (dashboard).
   - Di dashboard, user bisa memilih menu **Country** atau **Category**.
   - User bisa **membuat, mengedit, atau menghapus** Country / Category (CRUD).
   - User juga bisa melakukan **logout** dari dashboard.

2. **API (REST)**

   - API hanya digunakan untuk pencarian dan kalkulasi freight (tidak ada CRUD country/category lewat API).
   - Semua endpoint API berada di `/api/...`.

---

### API Endpoints

#### Authentication

| Endpoint        | Method | Payload                                                                            | Keterangan                                                                    |
| --------------- | ------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `/api/register` | POST   | `{ "email": "user@mail.com", "password": "123456", "confirm_password": "123456" }` | Registrasi user baru , response berisi `token` yang dipakai untuk autentikasi |
| `/api/login`    | POST   | `{ "email": "user@mail.com", "password": "123456" }`                               | Login, response berisi `token` yang dipakai untuk autentikasi                 |

Untuk endpoint selain `register` dan `login`, request harus menyertakan header:

```
Authorization: Bearer <token>
```

---

| Endpoint           | Method | Query / Payload                                               | Keterangan                                                                                                                     |
| ------------------ | ------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `/api/countries`   | GET    | `search={query}`                                              | Cari country berdasarkan nama                                                                                                  |
| `/api/categories`  | GET    | `country_id={id}&search={query}`                              | Cari category di country tertentu (search opsional)                                                                            |
| `/api/destination` | GET    | `search={city}`                                               | Cari destination city                                                                                                          |
| `/api/calculate`   | POST   | JSON: `country_id`, `category_id`, `destination_id`, `weight` | Menghitung freight, response: `origin`, `destination`, `category_name`, `international_price`, `domestic_price`, `total_price` |
