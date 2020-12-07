<b>ANALIZATOR RUCHU DROGOWEGO</b>  
by Martyna, Julia, Karolina  
  
Aplikacja ma na celu rozpoznawanie pojazdów na nagraniu oraz ich klasyfikację do 4 kategorii:  
1. Car   
2. Bus or Truck  
3. Two-wheelers  
4. Unknown (piesi)  

Aby uruchomić aplikację należy sklonować repozytorium oraz pobrać plik yolov3.weights:     
https://drive.google.com/drive/folders/1wUcYzKLiSWq7_02FdfR9dSi9-8qJySFF  
Pobrany plik następnie wkleić do folderu executable/gui. Wówczas można już uruchomić plik gui.exe z poziomu tego samego folderu.  
W folderze scripts znajdują się  dwa skrypty z rozszerzeniem .py, które składają się na tę aplikację. 
  
Z poziomu interfejsu graficznego użytkownik może wybrać video do analizy (w formacie mp4 i avi). Następnie rozpocząć analizę wybranego nagrania (przycisk start analizy).  
Po zakończeniu przetwarzania video zostanie wyświetlona informacja o zakończeniu analizy i użytkownik będzie miał możliwość wygenerowania pliu .csv zawierającego timestampy
wraz z liczbą zaobserwowanych pojazdów. Ponadto, możliwe będzie także odtworzenie ostatnio przetworzonego video w osobnym playerze. 
