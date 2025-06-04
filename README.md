[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=23&pause=700&color=00831BE9&background=FF3A3A00&width=1100&height=100&lines=Chess+Game+with+Stockfish+AI.;%D0%9F%D0%BE%D0%BB%D0%BD%D0%BE%D1%86%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F+%D1%88%D0%B0%D1%85%D0%BC%D0%B0%D1%82%D0%BD%D0%B0%D1%8F+%D0%B8%D0%B3%D1%80%D0%B0+%D1%81+%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%BC+%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81%D0%BE%D0%BC+%D0%B8+%D0%B8%D0%BD%D1%82%D0%B5%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D0%B5%D0%B9+%D0%B4%D0%B2%D0%B8%D0%B6%D0%BA%D0%B0+Stockfish.)](https://git.io/typing-svg)

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

### 2. Создайте виртуальное окружение и активируйте его
````bash
python3 -m venv venv
````
Linux/MacOS:
````bash
source venv/bin/activate
````
Windows:
````bash
venv\Scripts\activate
````
### 3. Установите зависимости

````bash
pip install -r requirements.txt
````

## ♟️ Установка Stockfish
Внимание: проект не содержит сам движок Stockfish. Его нужно установить отдельно.

#### 🔻 Шаги:
### 1.	Перейдите на https://stockfishchess.org/download
### 2.	Скачайте архив под вашу ОС:

    ОС	Ссылка
    macOS	stockfish-*-mac.zip
    Windows	stockfish-*-win.zip
    Linux	stockfish-*-linux.zip
### 3.	Распакуйте архив.
### 4.	Найдите исполняемый файл, например:
        •	stockfish-macos-m1-apple-silicon
        •	stockfish.exe
        •	stockfish
### 5.	Переименуйте файл в stockfish (или stockfish.exe на Windows).
### 6.	Поместите его в папку проекта:
        your_project/
        ├── main.py
        ├── stockfish/
        │   └── stockfish       ← сюда положите файл

### 🔐 Права на запуск (только macOS/Linux):
````bash
chmod +x stockfish/stockfish
````
### 🧪 Проверка

Запустите игру и сделайте ход. Если AI отвечает — всё настроено правильно ✅

### ⚙️ Конфигурация

В коде путь к движку задаётся так:\
Linux/MacOS:
````
STOCKFISH_PATH = "stockfish/stockfish"
````
Windows:
````
STOCKFISH_PATH = "stockfish/stockfish.exe"
````
