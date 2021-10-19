import { createStore } from 'vuex'
import axios from 'axios'
import router from '../router'

const task = {
    id: null,
    filename: null,
    video: null,
    status: null
}

export default createStore({
    state: {
        currentTask: task,
        tasksList: [],
        allTasksList: [],
        username: ''
    },
    mutations: {
        initialiseStore(state) {
            if (localStorage.getItem('success_login')) {
                state.username = localStorage.getItem('success_login');
            }
            if (JSON.parse(localStorage.getItem('tasks'))) {
                state.allTasksList = JSON.parse(localStorage.getItem('tasks'));
            }
            if (JSON.parse(localStorage.getItem('status'))) {
                state.tasksList = JSON.parse(localStorage.getItem('status'));
            }
        },
        resetState(state) {
            state.currentTask = task;
            state.tasksList = [];
            state.allTasksList = [];
            state.username = '';
            localStorage.removeItem('success_login');
            localStorage.removeItem('tasks');
            localStorage.removeItem('status');
        },
        setCurrentTask(state, value) {
            state.currentTask.id = value['task_id'];
            if (value['task_result'].filename !== null) {
                state.currentTask.filename = value['task_result'].filename;
            }
            if (value['task_result'].video !== null) {
                state.currentTask.video = value['task_result'].video;
            }
            state.currentTask.status = value['state'];
        },
        setTasksList(state, value) {
            localStorage.setItem('status', JSON.stringify(value));
            state.tasksList = value;
        },
        setAllTasksList(state, value) {
            localStorage.setItem('tasks', JSON.stringify(value));
            state.allTasksList = value;
        },
        setUsername(state, value) {
            localStorage.setItem('success_login', value);
            state.username = value;
        },
        clearTasksList(state) {
            state.tasksList = []
        }
    },
    actions: {
        getTask(context, urlTask) {
            axios.get('/result_task/' + urlTask)
                .then((response) => {
                    context.commit('setCurrentTask', response.data);
                    router.push({ path: `/status/${urlTask}`});
                })
                .catch(function () {
                    alert('Ошибка при загрузке задачи');
                });
        },
        getTasks(context) {
            axios.get('/all_result_tasks')
                .then((response) => {
                    context.commit('setAllTasksList', response.data);
                })
                .catch(function () {
                    alert('Ошибка при загрузке задач');
                });
        },
        loadTasks(context) {
            axios.get('/status_tasks')
                .then((response) => {
                    context.commit('setTasksList', response.data['tasks']);
                })
                .catch(function () {
                    alert('Ошибка при загрузке статуса задач');
                });
        },
        sendLogin(context, login_json) {
            axios.post('/api/login', login_json)
                .then((response) => {
                    alert(response.data.message);
                    context.commit('setUsername', response.data.username);
                    router.push(response.data.path);
                })
                .catch(function () {
                    alert('Ошибка при входе пользователя');
                });
        },
        sendRegister(context, register_json) {
            axios.post('/api/register', register_json)
                .then((response) => {
                    alert(response.data.message);
                    router.push(response.data.path);
                })
                .catch(function () {
                    alert('Ошибка при регистрации пользователя');
                });
        },
        onLogout(context) {
            axios.get('/logout')
                .then((response) => {
                    context.commit('resetState');
                    alert(response.data.message);
                    router.push(response.data.path);
                })
                .catch(function () {
                    alert('Ошибка при выходе пользователя');
                });
        }
    },
    modules: {
    }
})