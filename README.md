# Segmentator autorstwa Jakub Orzyłowski

Program automatyzuje proces segmentacji plików wav do formatu .eaf używanego 
przez program Elan. Oferowany jest interfejs graficzny jak i CLI.

## Instalacja

### Sposób #1 - zbudowanie i instalacja programu

1. Utworzyć folder, w którym chcemy przechowywać program.
2. Znajdując się w tym folderze użyć w wierszu poleceń najlepiej uruchomionym jako administrator, pobieramy repozystorium: `git clone https://github.com/JakubOrz/annotator-segmentator.git`, lub pobrać zip i wypakować
3. Sprawdzić czy mamy zainstalowany "pyinstaller" `pyinstaller --version`
4. Jeśli nie to można go zainstalować używając komendy `pip install pyinstaller`
5. Dokonać instalacji programu używając komendy `pyinstaller annotatorGUI.spec`
6. Utworzony zostanie folder dist/annotatorGUI a w nim oprócz bibliotek znajdować się będzie annotatorGUI.exe
7. Można utworzyć skrót i przenieść go w dowolne miejsce, byle nie przenosić głównego pliku exe.

### Sposób 2 - pobranie i pracowanie bezpośrednio na kodzie źródłowym

1. Wykonać punkt 1 i 2 ze sposobu #1.
2. Pobrać niezbędne biblioteki `pip install -r requirements.txt`
3. Wejść do folderu src/
4. Uruchomić wersję GUI lub CLI za pomocą polecenia `python annotatorGUI.py` lub `python annotatorCLI.py`

### Sposób #3 - pobranie wersji portable (działa na moim komputerze)

1. Pobrać i rozpakować [wersje portable](https://drive.google.com/drive/folders/1ToaknOVNLrQUsaXXrpHJ5a6KqcDlnIlJ?usp=sharing), nie gwarantuję, że będą wszędzie działać.

