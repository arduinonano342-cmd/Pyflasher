import PySimpleGUI as sg
import subprocess

# Словник з перекладами
LANGS = {
    "Укр": {"title": "Pyflasher Linux", "file": "Виберіть файл прошивки (.bin):", "baud": "Швидкість:", "mode": "Режим:", "erase": "Очистити пам'ять перед прошивкою (Erase Flash)", "flash": "Прошити", "exit": "Вихід", "log": "Лог роботи:", "error": "Помилка: Виберіть файл!", "start": "Починаю прошивку на швидкості", "done": "--- Прошивка завершена! ---"},
    "Рус": {"title": "ESP Flasher Linux", "file": "Выберите файл прошивки (.bin):", "baud": "Скорость:", "mode": "Режим:", "erase": "Очистить память перед прошивкой (Erase Flash)", "flash": "Прошить", "exit": "Выход", "log": "Лог работы:", "error": "Ошибка: Выберите файл!", "start": "Начинаю прошивку на скорости", "done": "--- Прошивка завершена! ---"},
    "Eng": {"title": "ESP Flasher Linux", "file": "Select firmware file (.bin):", "baud": "Baud rate:", "mode": "Mode:", "erase": "Erase flash before writing", "flash": "Flash", "exit": "Exit", "log": "Log:", "error": "Error: Select file!", "start": "Starting flash at speed", "done": "--- Flashing completed! ---"}
}

def get_layout(lang):
    text = LANGS[lang]
    return [
        [sg.Text("Language:"), sg.Combo(["Укр", "Рус", "Eng"], default_value=lang, enable_events=True, key="-LANG-")],
        [sg.Text(text["file"], key="-T_FILE-")],
        [sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("Bin files", "*.bin"),))],
        [sg.Text(text["baud"]), sg.Combo(["9600", "57600", "74880", "115200", "230400", "460800", "921600"], default_value="115200", key="-BAUD-"),
         sg.Text(text["mode"]), sg.Combo(["dio", "qio", "dout", "qout"], default_value="dio", key="-MODE-")],
        [sg.Checkbox(text["erase"], key="-ERASE-", default=False)],
        [sg.Button(text["flash"], key="-FLASH-"), sg.Button(text["exit"], key="-EXIT-")],
        [sg.Text(text["log"])],
        [sg.Output(size=(60, 10))]
    ]

current_lang = "Укр"
window = sg.Window(LANGS[current_lang]["title"], get_layout(current_lang))

while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, "-EXIT-"): break
    
    if event == "-LANG-":
        current_lang = values["-LANG-"]
        window.close()
        window = sg.Window(LANGS[current_lang]["title"], get_layout(current_lang))
        
    if event == "-FLASH-":
        file_path = values["-FILE-"]
        baud, mode, erase = values["-BAUD-"], values["-MODE-"], values["-ERASE-"]
        if not file_path:
            print(LANGS[current_lang]["error"])
            continue
        if erase:
            print("...")
            subprocess.run(["esptool.py", "--port", "/dev/ttyUSB0", "--baud", baud, "erase_flash"])
        print(f"{LANGS[current_lang]['start']} {baud}...")
        cmd = ["esptool.py", "--port", "/dev/ttyUSB0", "--baud", baud, "write_flash", "--flash_mode", mode, "--flash_size", "detect", "0x00000", file_path]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout: print(line, end="")
            print(f"\n{LANGS[current_lang]['done']}")
        except Exception as e: print(f"Error: {e}")

window.close()
