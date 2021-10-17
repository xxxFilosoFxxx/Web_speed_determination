import os

from flask import jsonify, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from backend.app import app
from backend.utils import operations_utils as op
from backend.utils.common_utils import process_log_string
# from backend.celery_tasks import send_task
from . import api_bp


@api_bp.route('/login', methods=['POST'])
def login():
    try:
        if current_user.is_authenticated:
            # Можно пробовать не отправлять username, так как он перезаписывает уже существующий
            return jsonify({'message': 'Вы уже авторизировались в системе',
                            'username': current_user.username, 'path': '/'})
        username = request.json.get('login', None)
        password = request.json.get('password', None)
        if op.check_validate_user(username=username, password=password):
            # Поскольку авторизация проходит не с помощью JWT токена
            # Ставим remember=True, иначе будут проблемы
            # Альтернатива -> поставить GET запрос и каждый раз проверять current_user
            op.check_login_user(username=username, remember=True)
            return jsonify({'message': 'Вы успешно авторизировались в системе',
                            'username': username, 'path': '/'})
        else:
            return jsonify({'message': 'Неверный ввод пользователя или пароля',
                            'username': None, 'path': '/login'})
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@api_bp.route('/register', methods=['POST'])
def register():
    try:
        if current_user.is_authenticated:
            return jsonify({'message': 'Вы уже зарегестрированы', 'path': '/'})
        username = request.json.get('login', None)
        password = request.json.get('password', None)
        reg = op.add_user_to_db(username=str(username), password=str(password))
        if reg:
            return jsonify({'message': 'Вы успешно зарегестрированы', 'path': '/login'})
        else:
            return jsonify({'message': 'Пользователь с таким именем уже существует', 'path': '/register'})
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


# @api_bp.route('/send_task', methods=['POST'])
# @login_required
# def for_send_task(countdown: int = 5):
#     try:
#         msisdn = request.json.get('msisdn', None)
#         radius = request.json.get('radius', None)
#         delta = request.json.get('delta', None)
#         username = request.json.get('username', None)
#
#         task = send_task.apply_async(args=[msisdn, radius, delta], countdown=countdown)
#         op.send_task_progress(task.id, username)
#         # print(f'Обработка данных пользователя {username}: {msisdn}, {radius}, {delta} через {countdown} секунд!')
#         return jsonify({'task_id': task.id, 'status': task.state}), 202
#     except Exception:
#         app.logger.exception(process_log_string(request))
#         raise
#
#
# @app.route('/uploads/<name>')
# def download_file(name):
#     try:
#         return send_from_directory(app.config["UPLOAD_FOLDER"], name)
#     except Exception:
#         app.logger.exception(process_log_string(request))
#         raise
#
#
# @api_bp.route('/load_video', methods=['POST'])
# @login_required
# def load_video():
#     try:
#         if 'file' not in request.files:
#             return jsonify({'file': 'Ошибка загрузки видео'})
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'file': 'Нет выбранного файла'})
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         # return jsonify({'file': 'Файл успешно обработался'}), 200
#         return redirect(url_for('download_file', name=filename))
#
#         msisdn = request.json.get('msisdn', None)
#         radius = request.json.get('radius', None)
#         delta = request.json.get('delta', None)
#         username = request.json.get('username', None)
#
#         task = send_task.apply_async(args=[msisdn, radius, delta], countdown=countdown)
#         op.send_task_progress(task.id, username)
#         # print(f'Обработка данных пользователя {username}: {msisdn}, {radius}, {delta} через {countdown} секунд!')
#         return jsonify({'task_id': task.id, 'status': task.state}), 202
#     except Exception:
#         app.logger.exception(process_log_string(request))
#         raise


@api_bp.route('/load_video', methods=['POST'])
@login_required
def load_video():
    try:
        if 'file' not in request.files:
            return jsonify({'file': 'Ошибка загрузки видео'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'file': 'Нет выбранного файла'})
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'file': filename}), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise
