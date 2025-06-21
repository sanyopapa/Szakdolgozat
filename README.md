# Fogászati rendelő webalkalmazás


Ez egy fogászati szakrendelő online időpontfoglaló és kezeléstörténet-kezelő rendszere Django keretrendszerben. Tartalmazza a szakdolgozat PDF-jét, a védéshez készült prezentációt, a tématervet és a teljes forráskódot.

## Készítette
- Sándor Márton (Programtervező Informatikus BSc hallgató, Szegedi Tudományegyetem)
- Témavezető: Antal Gábor adjunktus
- Dátum: 2025

## Tartalom
- `SZAKDOLGOZAT.pdf` – a szakdolgozat teljes dokumentuma.
- `prezentacio.pdf` – a védéshez készült diák.
- `tematerv.pdf` – a tématerv dokumentum.
- `rendelo/` – a Django-projekt és alkalmazás kódja.

## Követelmények
- Python 3
- pip
- virtualenv vagy venv
- Internet-kapcsolat a PayPal sandbox API eléréséhez, ha teszt fizetés kell.

<br><br>

# Beüzemelési útmutató 

## 1. Klónozd a repót

```sh
git clone <repo-url>
cd <repo-mappa>
```

## 2. Hozz létre virtuális környezetet (ajánlott: `myenv`)

```sh
python -m venv myenv
```

## 3. Aktiváld a virtuális környezetet

- **Windows:**
  ```sh
  myenv\Scripts\activate.bat
  ```
- **Linux/Mac:**
  ```sh
  source myenv/bin/activate
  ```

## 4. Adatbázis migrációk futtatása(ha kell)

```sh
python manage.py migrate
```

## 5. Szuperuser létrehozása (admin felülethez)

```sh
python manage.py createsuperuser
```
Kövesd a kérdéseket (felhasználónév, email, jelszó).

## 6. Szerver indítása

```sh
python manage.py runserver
```

## 7. Használat

- Nyisd meg a böngészőben: [http://localhost:8000/](http://localhost:8000/)
- Admin felület: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

**Tipp:**  
Ha a szerver fut, de valami hibát ír ki, ellenőrizd a `.env` fájlt, a függőségeket és hogy a virtuális környezet aktív-e.



