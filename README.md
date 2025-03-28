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
*Django, SQLite, HTML, JavaScript, CSS, Python*

# A Django keretrendszer
A Django egy magas szintű *Python* webkeretrendszer, amely támogatja a gyors fejlesztést és az egyszerű, jól átgondolt megoldásokat. Tapasztalt fejlesztők által készített, így számos webfejlesztési nehézséget megold, és lehetővé teszi, hogy a fejlesztő alkalmazás írására koncentráljon, anélkül, hogy újra fel kellene találnia a kereket. További pozitívuma, hogy ingyenes, és nyílt forráskódú.


