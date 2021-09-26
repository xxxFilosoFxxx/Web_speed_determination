import { createStore } from 'vuex'
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5dc33da (v2.0.1)

export default createStore({
  state: {
  },
  mutations: {
  },
  actions: {
<<<<<<< HEAD
=======
=======
import axios from 'axios'

// TODO: у каждого пользователя есть id -> по нему определеяем его список задач
// TODO: далее -> при отправке/удалении (и тд) обновляем список задач по uuid (reload -> mounted)
// TODO: параллельно -> обновляем данные в БД

const task = {
  id: null,
  uuid: null,
  msisdn: null,
  radius: null,
  delta: null,
  total: null,
  status: null
}

export default createStore({
  state: {
    currentTask: task,
    tasksList: [],
    username: ''
  },
  mutations: {
    resetState(state) {
      state.currentTask = task;
      state.tasksList = []
    },
    setCurrentTask(state, value) {
      state.currentTask = value;
    },
    setTasksList(state, value) {
      state.tasksList = value;
    },
    setUsername(state, value) {
      state.username = value;
    },
    clearTasksList(state) {
      state.tasksList = []
    },
    // reloadTaskList(state) {}
  },
  actions: {
    sendTask(context, msisdn, radius, delta) {
      axios.post('/send_task', {msisdn: msisdn, radius: radius, delta: delta})
          .then((response) => {
            // TODO: получение response от сервера (result)
          })
          .catch(function () {
            alert('Ошибка при отправке задачи в очередь');
          });
    },
    // TODO: добавить маршрут обработки
    loadTasks(context) {
      axios.get('/load_tasks_status')
          .then((response) => {
            context.commit('setTasksList', response.data['tasks_status']);
          })
          .catch(function () {
            alert('Ошибка при загрузке статуса задач');
          });
    },
    sendLogin(context, login, password, accept) {
      axios.post('/login', {'login': login, 'password': password, 'accept': accept})
          .then((response) => {
            context.commit('setUsername', response.data['username']);
          })
          .catch(function () {
            alert('Ошибка при входе пользователя');
          });
    },
    sendRegister(context, login, password) {
      axios.post('/register', {'login': login, 'password': password})
          .then((response) => {
            alert(response.data.message)
          })
          .catch(function () {
            alert('Ошибка при регистрации пользователя');
          });
    }
>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
  },
  modules: {
  }
})
