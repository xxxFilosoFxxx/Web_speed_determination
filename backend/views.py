from flask import render_template, url_for, jsonify, request, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from backend.app import app
from backend.utils import operations_utils as op
from backend.utils.common_utils import process_log_string
from celery_tasks import send_task


#class LoadFileVideo(APIView):
#    filename = 'file'
#    path = ''
#
#    def post(self, request):
#        self.path = settings.MEDIA_ROOT + '/' + str(request.FILES[self.filename])
#        default_storage.save(self.path, ContentFile(request.FILES[self.filename].read()))
#        print("[INFO] video saved successfully")
#        return Response({'success': 'Video load in media.'}, status=200)
#
#    @gzip.gzip_page
#    def live_video(self, process_file):
#        try:
#            print("[INFO] starting save video...")
#            self.path = settings.MEDIA_ROOT + '/' + str(process_file)
#            new_video = DetectionPeople(self.path)
#            return StreamingHttpResponse(new_video.translation_video(str(process_file)),
#                                         content_type='multipart/x-mixed-replace; boundary=frame')
#        except:
#            pass
            

@app.route('/')
@app.route('/index')
@login_required
def index():
    try:
        return render_template('index.html')
    except:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/login', methods=['POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        username = request.form['login']  # TODO: request.json.get
        password = request.form['password']
        remember = request.form['accept']
        if op.check_validate_user(username=username, password=password):
            op.check_login_user(username=username, remember=bool(remember))
            return jsonify({'username': username}), redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
    except:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/register', methods=['POST'])
def register():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        username = request.form['login']  # TODO: request.json.get
        password = request.form['password']
        op.add_user_to_db(username=username, password=password)
        flash('Вы успешно зарегестрированы')
        return jsonify({'message': 'Вы успешно зарегестрированы'}), redirect(url_for('login'))
    except:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/logout')
def logout():
    try:
        logout_user()
        flash('Вы вышли из системы')
        return redirect(url_for('login'))
    except:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/send_task', methods=['POST'])
@login_required
def for_send_task(countdown: int = 5):
    try:
        msisdn = request.json.get('msisdn', None)  # TODO: проверить на json
        radius = request.json.get('radius', None)
        delta = request.json.get('delta', None)
        task = send_task.apply_async(args=[msisdn, radius, delta], countdown=countdown)
        flash('Обработка данных {}, {}, {} через {} секунд!'.format(msisdn, radius, delta, countdown))
        # return jsonify({}), 202, {'location': url_for('task_status', task_id=task.id)}
        return jsonify({'task_id': task.id}), 202
    except:
        app.logger.exception(process_log_string(request))
        raise


# Результаты и сами данные в RabbitMQ не сохраняются
@app.route('/status/<task_id>', methods=['GET'])
@login_required
def task_status(task_id):
    try:
        task = send_task.AsyncResult(task_id)
        if task.state == 'PENDING':  # Цвет -> Желтый
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result  # None
                # 'status': 'Pending...'
            }
        elif task.state != 'FAILURE':  # Цвет -> Зеленый/Оранжевый
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,
                # 'status': task.info.get('status', '')
            }
            if task.state == 'SUCCESS':  # Цвет -> Зеленый
                # Запись в БД данных при успешно выполенной задаче
                op.send_success_result_task(uuid=task_id,
                                            msisdn=response['task_result']['msisdn'],
                                            radius=response['task_result']['radius'],
                                            delta=response['task_result']['delta'])
        else:
            # Ошибка на стороне сервера (или где-то еще)
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,
                'status': str(task.info)  # Цвет -> Красный
            }
        return jsonify(response), 200
    except:
        app.logger.exception(process_log_string(request))
        raise
