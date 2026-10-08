# Monitor Cen PL v0.3
Dedykowane parsery dla 8 źródeł. Wynik wymaga dopasowania EAN/PN do karty produktu. Ceny poniżej 20 PLN są odrzucane, co eliminuje m.in. koszty dostawy i raty.

## Wdrożenie
Zastąp całą zawartość repozytorium plikami z paczki. Następnie w Render uruchom Manual Deploy albo utwórz Blueprint z `render.yaml`. Po wdrożeniu odśwież przez Ctrl+Shift+R.

## Ważne
Status `zablokowano` oznacza odpowiedź HTTP 401/403/429. Parser nie obchodzi zabezpieczeń witryny. Dla Allegro rekomendowana docelowo jest oficjalna integracja API z własnymi poświadczeniami.
