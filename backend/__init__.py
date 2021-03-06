"""Основной функционал для рендеринга страниц и GET запросов."""

from backend.app import app
from backend.celery_tasks import video_processing
from backend.utils import operations_utils as op
from backend.utils.common_utils import process_log_string
from flask import jsonify, render_template, request, send_from_directory
from flask_login import current_user, login_required, logout_user


@app.route('/')
@login_required
def index():
    try:
        return render_template('index.html')
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/', defaults={'path': ''})
@app.route('/<path>')
def catch_all(path):
    try:
        return render_template("index.html")
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Вы успешно вышли из системы', 'path': '/login'})
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/status_tasks', methods=['GET'])
@login_required
def status_tasks():
    try:
        tasks_id = op.get_user_tasks(current_user.username)
        all_user_task = {}
        for uuid in tasks_id:
            all_user_task[uuid] = video_processing.AsyncResult(uuid).state
        response = {
            'tasks': all_user_task
        }
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/delete_task', methods=['GET'])
@login_required
def delete_task():
    try:
        task_id = request.args['task_id']
        op.delete_user_task_id(task_id)

        path = app.config['UPLOAD_FOLDER']
        filename = request.args['filename']
        op.delete_user_video(path, filename)
        response = {
            'filename': filename,
            'task_id': task_id
        }
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/all_result_tasks', methods=['GET'])
@login_required
def all_result_tasks():
    try:
        response = []
        tasks_id = op.get_user_tasks(current_user.username)
        for uuid in tasks_id:
            result = video_processing.AsyncResult(uuid)
            if result.state == 'PENDING':
                task = {
                    'task_id': uuid,
                    'filename': None,
                    'video': None,
                    'status': result.state
                }
                response.append(task)
            elif result.state != 'FAILURE':
                task = {
                    'task_id': uuid,
                    'filename': result.result['filename'],
                    'video': None,
                    'status': result.state
                }
                if result.state == 'SUCCESS':
                    task = {
                        'task_id': uuid,
                        'filename': result.result['filename'],
                        'video': result.result['video'],
                        'status': result.state
                    }
                response.append(task)
            else:
                task = {
                    'task_id': uuid,
                    'filename': None,
                    'video': None,
                    'status': result.state
                }
                response.append(task)
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/result_task/<task_id>', methods=['GET'])
@login_required
def result_task(task_id):
    try:
        task = video_processing.AsyncResult(task_id)
        if task.state == 'PENDING':  # Цвет -> Синий
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': {
                    'filename': None,
                    'video': None
                },
                'info': str(task.info)  # Содержит task.result в формате json
            }
        elif task.state != 'FAILURE':  # Цвет -> Зеленый/Желтай
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,
                'info': str(task.info),
            }
            if task.state == 'SUCCESS':  # Цвет -> Зеленый
                # Здесь можно получить результат после выполнения
                response = {
                    'task_id': task_id,
                    'state': task.state,
                    'task_result': task.result,
                    'info': str(task.info),
                    'date_done': task.date_done.strftime('%H:%M | %d %B %Y')
                }
        else:  # Цвет -> Красный
            # Ошибка на стороне сервера (или где-то еще)
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': {
                    'filename': None,
                    'video': None
                },
                'info': str(task.info)  # Информация об ошибке
            }
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/source_video/<video>', methods=['GET'])
@login_required
def source_video(video):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename=video,
                                   as_attachment=False, mimetype='video/mp4')
    except Exception:
        app.logger.exception(process_log_string(request))
        raise
