## Szegedi Tudományegyetem  
## Informatikai Intézet  

**Fogászati rendelő webalkalmazás implementálása**  
**Django keretrendszerben**

## SZAKDOLGOZAT  


**Készítette:**  
Sándor Márton 

*Programtervező informatikus BSc szakos hallgató*

**Témavezető:**  
Antal Gábor  

*Szeged, 2025*


# Tartalmi összefoglaló

## A téma megnevezése: 
Fogászati rendelő webalkalmazás implementálása Django keretrendszerben

## A megadott feladat megfogalmazása
A Django keretrendszer által nyújtott előnyök megismerése, felhasználása a 
fogászati rendelő időpontfoglalási rendszerének fejlesztéséhez. Az alkalmazásnak 
rendelkeznie kell felhasználói, orvosi, és adminisztrátori felülettel.
Meg kell valósítani az online időpontfoglalás, és az online fizetés lehetőségét.
Az orvosoknak meg kell valósítani egy felületet amivel vissza tudják nézni a 
páciens kezeléstörténetét. Az adatokat pedig FHIR szabvány szerint kell tárolni,
hogy bármilyen más egészségügyi rendszerrel kompatibilis legyen.

## Megoldási mód
Megismerkedtem a *Django* keretrendszerrel, annak felépítésével. Megterveztem a rendelő webalkalmazásának adatbázis-struktúráját, amely tartalmazza a páciensek, orvosok, kezelések és időpontfoglalások moduljait. Az alkalmazás reszponszív felhasználói felületét modern *CSS* megoldásokkal építettem ki, míg a backend részben a *Django admin* és *REST API*-k biztosítják az adatok hatékony kezelését. Emellett integráltam a *PayPal* fizetési rendszert az online fizetések lebonyolításához. A fejlesztés során a projektet GitHubon verzióztam, biztosítva ezzel a kód stabilitását és könnyű karbantarthatóságát.

## Alkalmazott eszközök, módszerek:
*Git, Github, Django, SQLite, HTML, JavaScript, CSS, Python*

## Elért eredmények:
Megismertem a *Django*t, és az általa nyújtott lehetőségeket, a *PayPal* integrációt, 
a *Python* nyelvet, az *FHIR* szabványt, és a webfejlesztést. Sikeresen működik az általam integrált időpontfoglalási és fizetési rendszer. 

## Kulcsszavak: 
*Django, SQLite, HTML, JavaScript, CSS, Python, ORM*

# A Django keretrendszer
A Django egy magas szintű *Python* webkeretrendszer, amely támogatja a gyors fejlesztést és az egyszerű, jól átgondolt megoldásokat. Tapasztalt fejlesztők által készített, így számos webfejlesztési nehézséget megold, és lehetővé teszi, hogy a fejlesztő alkalmazás írására koncentráljon, anélkül, hogy újra fel kellene találnia a kereket. További pozitívuma, hogy ingyenes, és nyílt forráskódú.
[1]

# Tartalomjegyzék

# Az MVT programszervezési minta
Django projekt lévén az alkalmazás az MVT (Model View Template) design pattern alapelveit kell, hogy kövesse. Ez áll a model-ből, ahol az adatbázis struktúrájáját építjük fel, a view-ból, ami lényegében a projekt azon része, ahol a háttérfolyamatok futnak, és a template-ből, ami a felhasználói felületet tartalmazza. Ez a kapcsolata a felhasználónak az alkalmazással. 

## Model

A Model-ek a Django alkalmazáson belüli adatszerkezet kezelését és interakcióját irányítják, így a Django alkalmazások alapját képezik, mivel az adatok kritikus szerepet játszanak.

A Django Model-ek egy erőteljes, Objektum-Relációs Leképezést (ORM: Object-Relational Mapping) megvalósító funkciót használnak, amely áthidalja a szakadékot a relációs adatbázis és a Python kód között. Ez a leképezés a Python objektumokat (osztályokat) adatbázis táblákká alakítja, az osztályok attribútumait oszlopokká, és az egyes példányokat a táblák soraivá.

Az ORM egyik nagy előnye, hogy lehetővé teszi az adatbázissal való interakciót Python objektumokon keresztül, anélkül, hogy SQL lekérdezéseket kellene írnunk.

A Django Model-ek összegzik az összes adatbázissal kapcsolatos logikát és meghatározzák az adatbázis szerkezetét, mint egy tervrajzot annak, hogy milyen adatokat szeretnénk tárolni.[2]

## View

Ha az MVC modellhez szeretnénk hasonlítani, akkor az MVT modellben a View hasonló, mint az MVC-ben a Controller.

A Django view-k felelősek a felhasználói kérések feldolgozásáért és a válaszok visszaküldéséért. Híd szerepét töltik be a Model és a Template között: Adatokat gyűjtenek a Model-ből, logikai műveleteket (például bizonyos kritériumok alapján végzett lekérdezéseket) hajtanak végre rajtuk, majd az eredményeket átadják a Template-nek a megjelenítéshez.

A View-kat függvényekként vagy osztály alapú View-ként is megírhatjuk, attól függően, hogy az alkalmazásunk komplexitása és követelményei melyik megközelítést igénylik.[2]

## Template

A Django Template-ek feladata, hogy a böngészőben megjelenítendő végső HTML kimenetet rendereljék. Meghatározzák, miként kell az adatokat bemutatni, HTML és a Django sablonnyelvének kombinációjával. 

A Django sablonnyelv template tageket (`{% %}`) és template változókat (`{{ }}`) alkalmaz, amelyek lehetővé teszik, hogy a sablon HTML kódjában Django módba lépjen, és így hozzáférjen a View-kban definiált változókhoz, illetve vezérlési struktúrákat használjon a megjelenítés szabályozására.

A sablonok továbbá formázhatók CSS-sel, illetve bármely kedvelt CSS keretrendszerrel, hogy a felhasználói felület mégszebb legyen. Emellett animálhatók is JS segítségével.[2]

# Alkalmazás struktúrája

Egy Django projekt esetében a projekt felépítése modulárisan, egy vagy több alkalmazásból (app) áll, melyek mindegyike egy adott funkcionális területért felel. A szakdolgozatom esetében a "rendelo" mappa tartalmazza a teljes webalkalmazás forráskódját.

A "rendelo" mappa a következő részekből áll:  
- Gyökérszint:
  - *manage.py:* A Django projekt parancssori kezelője, amely a fejlesztési feladatok (például migrációk futtatása, szerver indítása) végrehajtását segíti.  
  - *db.sqlite3:* Az alapértelmezett, fejlesztési környezetben használt SQLite adatbázis fájlja.
  
- Projekt főkönyvtára ("rendelo"):
  Itt találhatók a projekt globális beállításait és konfigurációs fájljait, mint például a *settings.py*, *urls.py*, *wsgi.py* és *asgi.py*. Ezek a fájlok felelősek az alkalmazás működésének alapvető paramétereinek meghatározásáért, az útvonalak kezeléséért és a szerverrel való kommunikációért.

- Alkalmazás könyvtára ("rendeloweboldal"): 
  Ez a rész tartalmazza a rendszer egyes moduljait, amelyek a következő fő komponensekből állnak:
  - *models.py:* Az adatbázis szerkezetét definiáló modellek, melyek meghatározzák a páciensek, orvosok, kezelések, időpontfoglalások és fizetési státuszok struktúráját.
  - *views.py:* A felhasználói kérések feldolgozásáért és az üzleti logika megvalósításáért felelős réteg, amely összeköti a modelleket a sablonokkal.
  - *forms.py:* Az űrlapok és azok validációs szabályainak definíciója, melyek révén az adatbevitel és ellenőrzés történik.
  - *urls.py:* Az alkalmazás specifikus URL-konfigurációja, amely a különböző view-k elérését biztosítja.
  - *admin.py:* A Django beépített admin felület konfigurációját tartalmazza, amely az adatok egyszerű kezelését teszi lehetővé.
  - *migrations/*: Az adatbázis változásait követő migrációs fájlokat tartalmazza, dokumentálva a modellek módosításait.
  - *static/* és *templates/*: A statikus fájlokat (CSS, JavaScript, és az alkalmazás designjához tartozó képek) illetve a HTML template-eket rendszerezi, amelyek a felhasználói felület megjelenítéséért felelősek.

A projekt kialakítása moduláris és átlátható, mely lehetővé teszi a fejlesztés, karbantartás és bővítés egyszerű kezelését.

Emellett a projekt verziókezelése GitHubon történik, így a fejlesztési változtatások könnyen nyomon követhetők, és a kód stabilitása biztosított. 

# Irodalomjegyzék
- [1] *Django: The web framework for perfectionists with deadlines https://www.djangoproject.com*

- [2] *How Django's MVT Architecture Works: A Deep Dive into Models, Views, and Templates https://www.freecodecamp.org/news/how-django-mvt-architecture-works/*

# Nyilatkozat

Alulírott Sándor Márton Programtervezó informatikus BSc szakos hallgató, kijelentem, hogy a dolgozatomat a Szegedi Tudományegyetem, Informatikai Intézet Szoftverfejlesztés Tanszékén készítettem, Programtervezó informatikus BSc diploma megszerzése érdekében. 
Kijelentem, hogy a dolgozatot más szakon korábban nem védtem meg, saját munkám eredménye, és csak a hivatkozott forrásokat (szakirodalom, eszközök, stb.) használtam fel. Tudomásul veszem, hogy szakdolgozatomat / diplomamunkámat a Szegedi Tudományegyetem Diplomamunka Repozitóriumában tárolja.



