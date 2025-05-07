# ss_scraper

## Projekta uzdevums
Projekta mērķis ir izveidot tīmekļa skrāpēšanas rīku, kas automātiski iegūst automašīnu sludinājumus no ss.lv. Programma ļauj lietotājam norādīt noteiktas mašīnas marku, cenu apjomu un maksimālo lapu skaitu, ko skrāpēt, un vaicā vai lietotājs vēlās saglabā iegūtos datus CSV failā.

## Izmantotās Python bibliotēkas un to pielietojums
Projekta izstrādes laikā tiek izmantotas sekojošas Python bibliotēkas:
- **`requests`**: Lai veiktu HTTP pieprasījumus un iegūtu tīmekļa lapas HTML saturu.
- **`csv`**: Lai saglabātu iegūtos datus CSV failā strukturētā formātā.
- **`os`**: Lai pārvaldītu failu sistēmas operācijas, piemēram, direktoriju izveidi rezultātu saglabāšanai (piem. results/{filename}.csv).
- **`BeautifulSoup`**: Lai analizētu un parsētu HTML saturu, ja nepieciešams.
Šīs bibliotēkas tiek izmantotas, lai nodrošinātu datu iegūšanu, apstrādi un saglabāšanu.

## Izmantotās datu struktūras
Projekta laikā tiek izmantotas Python iebūvētās datu struktūras:
- **`list`**: Lai saglabātu visu sludinājumu saites (`all_links`) un apstrādātos rezultātus (`results`).
- **`tuple`**: Lai strukturēti saglabātu katra sludinājuma informāciju (mašīnas nosaukumu, cenu un sludinājuma linku) pirms to ierakstīšanas CSV failā.

## Programmatūras izmantošanas metodes
1. **Programmas palaišana**:
   - Palaidiet skriptu, izmantojot Python interpretatoru:  
     ```bash
     python ss.py
     ```
2. **Lietotāja ievade**:
   - Programma pieprasa lietotājam ievadīt mašīnas marku, minimālo un maksimālo cenu apjomu, un maksimālo lapu skaitu, ko skrāpēt.
3. **Datu iegūšana**:
   - Programma automātiski ģenerē saites uz sludinājumu lapām, iegūst HTML saturu un parsē mašīnu nosaukumus, un cenas (izvēlētajā intervālā).
4. **Rezultātu saglabāšana**:
   - Iegūtos datus ir iespējams saglabat kā CSV failu direktorijā `results`. Faila nosaukums ir atkarīgs no izvēlēto marku, piemēram, `results/{brand}_cars.csv`, kur {brand} ir izvēlētā marka (peim. results/bmw_cars.csv). Failu tikai saglabā, ja lietotājs ir to apstiprinājis.
5. **Rezultātu pārskatīšana**:
   - Terminālā tiek izvadīti visi atrastie sludinājumi ar attiecīgiem datiem, kā arī ir iespējams atvērt izveidoto CSV failu, lai apskatītu iegūtos datus.

## Demonstrācijas video
### [Skatīt programmas darbības video](https://drive.google.com/file/d/1opBXSi0BkO5QFW_42yb2kg2HCSkjN6V8/view?usp=sharing)
Piezīme: Īsti nesapratu kādēļ, bet saglabājot datus uz manu windows datoru .csv failā, eiro simboli tika uzrādīti ka excel utf-8 sintakse. Diemžēl, nebiju spējīgs to izlabot, toties visur citur dati tika saglabāti pareizi, kā bija redzams notepad. Linux sistēmā, saglabājot .csv failā gan rādijās attiecīgie eiro simboli.