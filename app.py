import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory, jsonify
from threading import Thread, Lock

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

progress_lock = Lock()
progress = 0
total_frames = 1  # Избегаем деления на ноль
video_path = None

def create_zebra_pattern(width, height):
    zebra = np.zeros((height, width, 3), dtype=np.uint8)
    zebra[(np.indices((height, width)).sum(axis=0) // 10) % 2 == 0] = [255, 255, 255]  # Белый
    zebra[(np.indices((height, width)).sum(axis=0) // 10) % 2 == 1] = [0, 0, 0]  # Черный
    return zebra


def add_zebra_to_frame(frame, zebra_pattern, mode, black_threshold=0, white_threshold=255):
    height, width, _ = frame.shape
    mask_bright = (frame.max(axis=2) >= white_threshold)
    mask_dark = (frame.min(axis=2) <= black_threshold)
    if mode == 'highlight':
        frame[mask_bright] = zebra_pattern[mask_bright]
    elif mode == 'blackout':
        frame[mask_dark] = zebra_pattern[mask_dark]
    elif mode == 'both':
        mask = mask_bright | mask_dark
        frame[mask] = zebra_pattern[mask]
    return frame


def process_video(input_file_path, mode, black_threshold_value, white_threshold_value):
    global video_path, progress, total_frames

    cap = cv2.VideoCapture(input_file_path)
    if not cap.isOpened():
        raise ValueError("Не удалось открыть видеофайл.")

    fps = cap.get(cv2.CAP_PROP_FPS) # количество кадров в секунду
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    zebra_pattern = create_zebra_pattern(width, height)
    output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f"processed_{os.path.basename(input_file_path)}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Используем mp4v кодек
    out = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    progress = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = add_zebra_to_frame(frame.copy(), zebra_pattern, mode,
                                             black_threshold=black_threshold_value,
                                             white_threshold=white_threshold_value)
        out.write(processed_frame)

        # Обновляем прогресс
        with progress_lock:
            progress += 1


        percent_complete = (progress / total_frames) * 100
        print(f"Processing: {min(percent_complete, 100):.2f}%")

    cap.release()
    out.release()

    with progress_lock:
        video_path = output_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        mode = request.form.get('mode', 'both')  # Получаем режим
        black_threshold_value = int(request.form.get('black_threshold', 0))
        white_threshold_value = int(request.form.get('white_threshold', 255))

        if file:
            input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_file_path)

            # Запускаем обработку видео в отдельном потоке
            thread = Thread(target=process_video,
                            args=(input_file_path, mode, black_threshold_value, white_threshold_value))
            thread.start()

            return render_template('index.html', processing=True)

    return render_template('index.html', processing=False)

@app.route('/progress') #определяет маршрут для URL
def get_progress():
    with progress_lock:
        percent_complete = (progress / total_frames) * 100
        return jsonify(progress=min(percent_complete, 100))  # Ограничиваем прогресс до 100%

@app.route('/video') #отвечает за отправку обработанного видеофайла клиенту
def serve_video():
    global video_path
    if video_path and os.path.exists(video_path):
        output_path = video_path  # Сохраняем путь к видео
        with progress_lock:
            # Сбрасываем прогресс после завершения обработки
            global progress
            progress = 0
            video_path = None
        return send_from_directory(app.config['OUTPUT_FOLDER'], os.path.basename(output_path))

    return '', 404

@app.errorhandler(Exception) #функция-обработчик
def handle_exception(e):
    return f"Произошла ошибка: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
