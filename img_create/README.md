# mockup-maker-imker


## Opis
Nakładanie obrazu do ramki tableta/smartfona<br />

## Użycie
... overlay.py <ścieżka do obrazu> <typ urządzenia><br />

Możliwy typ urządzenia:<br />
TABLET_01<br />
TABLET_02<br />
PHONE_01<br />
AUDIOBOOK_TABLET_01<br />
PHONE_TABLET_01<br />
AUDIOBOOK_PHONE_TABLET_01<br />

## Dodawanie nowego typu urządzenia

overlay_image_under(path_image, path_frame, desired_size, pts1, pts2, file_name)<br />
<br />
Dla jednego urządzenia z wyciętym ekranem bez ucinania rogów obrazu - ramka jest wklejana na <br />
obraz.<br />
path_image <- ściezka do nakładanego obrazka<br />
path_frame <- ściezka do obrazu ramki urządzenia<br />
desired_size <- szerokość i wysokość obrazu path_frame w px<br />
pts1 <- pozycje rogów obrazu w px path_image po zmianie wielkości do desired_size. Format <br />
punktów [szerokość, wysokość], zaczynając od lewego górnego rogu [0,0], prawy górny [x, 0], <br />
lewy dolny [0, y], prawy dolny [x, y].<br />
pts2 <- pozycje rogów obrazu path_image na obrazie path_frame w px<br />
file_name <- nazwa pliku do zapisu<br />
<br />
<br />
overlay_image_over(path_image, path_frame, desired_size, pts1, pts2, file_name)<br />
<br />
Dla jednego urządzenia, bez ucinania rogów - obraz jest wklejany na ramkę<br />
path_image <- ściezka do nakładanego obrazka<br />
path_frame <- ściezka do obrazu ramki urządzenia<br />
desired_size <- szerokość i wysokość obrazu path_frame w px<br />
pts1 <- pozycje rogów obrazu w px path_image po zmianie wielkości do desired_size. Format <br />
punktów [szerokość, wysokość], zaczynając od lewego górnego rogu [0,0], prawy górny [x, 0], <br />
lewy dolny [0, y], prawy dolny [x, y].<br />
pts2 <- pozycje rogów obrazu path_image na obrazie path_frame w px<br />
file_name <- nazwa pliku do zapisu<br />
<br />
<br />
overlay_two_images(path_image, path_frame, desired_size, pts1, pts2, pts3, pts4, file_name)<br />
<br />
Dla dwóch urządzeń, bez ucinania rogów - ramka jest wklejana na obrazy.<br />
path_image <- ściezka do nakładanego obrazka<br />
path_frame <- ściezka do obrazu ramki urządzenia<br />
desired_size <- szerokość i wysokość obrazu path_frame w px<br />
pts1 <- pozycje rogów obrazu w px path_image po zmianie wielkości do desired_size. Format <br />
punktów [szerokość, wysokość], zaczynając od lewego górnego rogu [0,0], prawy górny [x, 0], <br />
lewy dolny [0, y], prawy dolny [x, y].<br />
pts2 <- pozycje rogów obrazu path_image na obrazie path_frame w px. Wklejany w warstwie <br />
poniżej następnego obrazu.<br />
pts3 <- pozycje rogów obrazu w px path_image po zmianie wielkości do desired_size. Format <br />
punktów [szerokość, wysokość], zaczynając od lewego górnego rogu [0,0], prawy górny [x, 0], <br />
lewy dolny [0, y], prawy dolny [x, y].<br />
pts4 <- pozycje rogów obrazu path_image na obrazie path_frame w px. Wklejany w warstwie <br />
powyżej poprzedniego obrazu.<br />
file_name <- nazwa pliku do zapisu<br />
<br />
<br />
overlay_two_rounded_images(path_image, path_frame, desired_size, pts1, pts2, pts3, pts4, <br />
cut_corner_back, cut_corner_front, size_cut_back, size_cut_front, file_name)<br />
<br />
Dla dwóch urządzeń, z ucinaniem rogów - ramka jest wklejana na obrazy.<br />
path_image <- ściezka do nakładanego obrazka<br />
path_frame <- ściezka do obrazu ramki urządzenia<br />
desired_size <- szerokość i wysokość obrazu path_frame w px<br />
pts1 <- pozycje rogów obrazu w px path_image po zmianie wielkości do desired_size. Format <br />
punktów [szerokość, wysokość], zaczynając od lewego górnego rogu [0,0], prawy górny [x, 0], <br />
lewy dolny [0, y], prawy dolny [x, y].<br />
pts2 <- pozycje rogów obrazu path_image na obrazie path_frame w px. Wklejany w warstwie <br />
poniżej następnego obrazu.<br />
pts3 <- pozycje rogów obrazu w px path_image po zmianie wielkości do desired_size. Format <br />
punktów [szerokość, wysokość], zaczynając od lewego górnego rogu [0,0], prawy górny [x, 0], <br />
lewy dolny [0, y], prawy dolny [x, y].<br />
pts4 <- pozycje rogów obrazu path_image na obrazie path_frame w px. Wklejany w warstwie <br />
powyżej poprzedniego obrazu.<br />
cut_corner_back <- czy ściąć w obrazie będacym w najniższej warstwie rogi. True/False<br />
cut_corner_front <- czy ściąć w obrazie będącym w wartswie powyżej poprzedniego obrazu rogi. <br />
True/False<br />
size_cut_back <- promień cięcia rogu w najniższej warstwie<br />
size_cut_front <- promień cięcia rogu w wyższej warstwie<br />
file_name <- nazwa pliku do zapisu<br />
