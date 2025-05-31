
[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Chess Game with Stockfish AI)](https://git.io/typing-svg)
Полноценная шахматная игра с графическим интерфейсом и интеграцией мощного шахматного движка **Stockfish**.

---

## 🚀 Возможности

- Игра против сильного AI (Stockfish)
- Графическая доска (Pygame)
- Автоматическая проверка правил ходов
- Возможность менять уровень сложности AI

---

## 🛠 Установка

### 1. Клонируйте репозиторий

````bash
git clone https://github.com/kl1z/SimpleChess.git
cd SimpleChess
````
2. Установите зависимости

````bash
pip install -r requirements.txt
````

♟️ Установка Stockfish
Внимание: проект не содержит сам движок Stockfish. Его нужно установить отдельно.

🔻 Шаги:
    1.	Перейдите на https://stockfishchess.org/download
    2.	Скачайте архив под вашу ОС:

    ОС	Ссылка
    macOS	stockfish-*-mac.zip
    Windows	stockfish-*-win.zip
    Linux	stockfish-*-linux.zip

    3.	Распакуйте архив.
    4.	Найдите исполняемый файл, например:
        •	stockfish-macos-m1-apple-silicon
        •	stockfish.exe
        •	stockfish
    5.	Переименуйте файл в stockfish (или stockfish.exe на Windows).
    6.	Поместите его в папку проекта:
        your_project/
        ├── main.py
        ├── stockfish/
        │   └── stockfish       ← сюда положите файл

🔐 Права на запуск (только macOS/Linux):
````bash
chmod +x stockfish/stockfish
````
🧪 Проверка

Запустите игру и сделайте ход. Если AI отвечает — всё настроено правильно ✅

⚙️ Конфигурация

В коде путь к движку задаётся так:\
Linux/MacOS:
````
STOCKFISH_PATH = "stockfish/stockfish"
````
Windows:
````
STOCKFISH_PATH = "stockfish/stockfish.exe"
````
