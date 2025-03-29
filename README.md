
# Video Zebra Processing Application

## Функциональность

Данное приложение позволяет загружать видеофайлы и добавлять к ним эффект зебры в областях пересвета (overexposure) и провалов в черное (underexposure). Основные функции включают:

- Поддержка трех режимов обработки видео:
  - Пересвет (highlight)
  - Провал (blackout)
  - Оба (both)
- Настройка порогов для черного и белого уровня (threshold) для точной обработки.
- Реализация через веб-интерфейс с возможностью выбора параметров и загрузки обработанного видео.
- Прогресс-бар для отображения состояния обработки видео.

## Предварительные требования

Перед началом работы убедитесь, что у вас установлены следующие компоненты:

- **Python 3.10** или выше
- **Docker** (если вы планируете запускать приложение в контейнере)
- **Flask**, **OpenCV**, и **numpy**

## Установка

### 1. Установка через локальную среду

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/tori-da-vi/computer_graphics_firstHW
    cd computer_graphics_firstHW
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Запустите приложение:
    ```bash
    python app.py
    ```

### 2. Установка и запуск через Docker

1. Соберите Docker-образ:
    ```bash
    docker-compose build
    ```

2. Запустите приложение:
    ```bash
    docker-compose up
    ```

## Запуск приложения

Приложение будет доступно по адресу: [http://localhost:5001](http://localhost:5001).

## Использование

1. Загрузите видеофайл через веб-интерфейс.
2. Выберите режим:
   - **Оба**: Зебра будет применена к областям как пересвета, так и провалов.
   - **Пересвет**: Зебра будет применена только к пересвеченным областям.
   - **Провал**: Зебра будет применена только к областям провала в черное.
3. Установите пороги для черного и белого уровней (значения от 0 до 255).
4. Нажмите кнопку "Загрузить видео" и дождитесь завершения обработки.
5. Когда видео будет обработано, скачайте его по ссылке.

## Зависимости

- Flask>=2.0
- numpy>=1.21,<1.23; python_version < '3.11'
- numpy>=1.23; python_version >= '3.11'
- opencv-python==4.8.0.74
