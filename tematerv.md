# Tématerv - Sándor Márton



## Személyes adatok

Név: Sándor Márton

Neptun: BFAM77

E-mail: sandormarton265@gmail.com

Szak: Programtervező informatikus Bsc

Végzés várható ideje: 2025. nyár



## A szakdolgozat tárgya

A szakdolgozatom egy fogorvosi rendelő számára készített webalkalmazás fejlesztéséről szól. Az alkalmazás lehetőséget biztosít a páciensek számára online időpontfoglalásra, valamint a kezelési előzményeik nyomon követésére. A rendszer lehetővé teszi az orvosok és adminisztrátorok számára az időpontok kezelését és a páciensek adataihoz való hozzáférést.

A felhasználók különböző jogosultsági szinteken érhetik el a rendszert: a páciensek foglalhatnak időpontot, az adminisztrátorok pedig menedzselhetik az időpontokat és a rendelő napi ütemezését. A rendszer automatikus email értesítéseket is küld a közelgő foglalásokról, és biztosítja a felhasználók számára a biztonságos hozzáférést. A felhasználó lehetőséget kap az online előre fizetésre is. Az alkalmazás webes felületen működik.

Funkciók:
 - Felhasználói regisztráció és bejelentkezés: A páciensek és adminisztrátorok biztonságos belépési rendszeren keresztül férhetnek hozzá az alkalmazáshoz.
 - Időpontfoglalás: A páciensek időpontot foglalhatnak a rendelő fogorvosaihoz, megadott időintervallumok alapján. A legközelebbi időpontot ajánlja fel, és optimalizálja az időpontokat, hogy egymás után következzenek, és minél kevesebb szünet legyen közöttük.
 - Értesítési rendszer: Automatikus email értesítések küldése a foglalások visszaigazolásáról és a közelgő időpontokról.
 - Felhasználói profilok: A páciensek megtekinthetik és szerkeszthetik személyes adataikat.
 - Kezelési előzmények: A fogorvosok rögzíthetik a páciensek korábbi kezeléseit, amelyeket a páciensek bármikor megtekinthetnek.
 - Adminisztrációs felület: Az adminisztrátorok és fogorvosok kezelhetik a foglalásokat és a rendelő beosztását.
 - Reszponzív webes felület: Az alkalmazás asztali gépen és mobileszközön is egyaránt jól működik.
 - Online fizetés integrálása: A SimplePay rendszer segítségével a páciensek lehetőséget kapnak arra, hogy előre kifizessék a kezelést az időpontfoglalás során.

## Használni kívánt technológiák

 - Backend: Python (Django) - Robusztus, jól támogatott keretrendszer, amely gyors fejlesztést biztosít.
 - Adatbázis: MySQL - Megbízható, könnyen kezelhető relációs adatbázis-kezelő rendszer, amely jól skálázható és megfelelő teljesítményt biztosít.
 - Adatmodell: FHIR (Fast Healthcare Interoperability Resources) szabvány alapján, amely biztosítja az egészségügyi adatok szabványos tárolását és kezelését.
 - Frontend: HTML, CSS, JavaScript - Felhasználóbarát és reszponzív webes felület létrehozása.
 - Email küldés: Python smtplib - Automatikus értesítések küldésére emailben.
 - Authentikáció és jogosultság kezelés: Django Authentication - Felhasználói bejelentkezés és jogosultságkezelés.

## Tervezett ütemezés

### 2024. szeptember  
 - A projekt specifikációk véglegesítése, követelmények kidolgozása.  
 - Frontend fejlesztés megkezdése: alapvető felhasználói felület kialakítása HTML, CSS, és JavaScript segítségével.

### 2024. október  
 - Frontend fejlesztés folytatása: reszponzív dizájn és interaktív elemek hozzáadása.  
 - A felhasználói regisztráció és bejelentkezési oldalak kialakítása.

### 2024. november  
 - Backend fejlesztés megkezdése: adatbázis (MySQL) struktúrájának kialakítása.  
 - A felhasználói adatok kezelése, bejelentkezési és regisztrációs funkciók összekapcsolása a backenddel.

### 2024. december  
 - Időpontfoglalási rendszer backend fejlesztése.  
 - Az időpontfoglalás frontend és backend integrációja.

### 2025. január  
 - Értesítési rendszer implementálása (automatikus email küldés).  
 - Kezelési előzmények kezelése az adatbázisban és a felhasználói felületen.

### 2025. február  
 - Teljes alkalmazás tesztelése.  
 - Hibajavítások és finomhangolás.  
 - Adatvédelem és biztonsági funkciók megvalósítása.

### 2025. március  
 - Végső hibajavítások és tesztelés.  
 - Szakdolgozat dokumentáció megírása.

### 2025. április  
 - Szakdolgozat befejezése és leadása.