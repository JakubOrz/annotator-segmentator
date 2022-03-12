import sys
from core import EafFile

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python3 annotatorCLI wav_file.wav output_file")
        sys.exit(1)

    wav_file = sys.argv[1]
    output_file = sys.argv[2]

    if not wav_file.endswith(".wav"):
        print("Podany plik wejścia jest niepoprawnego formatu")
        sys.exit(1)

    file = EafFile(wav_file, output_file)
    result: dict = file.start_processing()

    if result['success']:
        print("Przygotowanie pliku zakończone")
    else:
        print("Coś poszło nie tak")

    sys.exit(0)
