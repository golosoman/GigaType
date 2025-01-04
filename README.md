# GigaType ⌨️🚀

## ★ О проекте

GigaType — веб-приложение, предназначенное для тренировки навыка слепой печати с функциями администратора.

### Основной функционал приложения

- Тренировка слепой печати 🖥️
- Создание и редактирование упражнений ✍️
- Настройка уровней сложности 🔄
- Управление пользователями (добавление и блокировка) 👤
- Сбор статистики для обучаемых и администраторов 📊

## 🖥️ Используемые технологии

### Фронтенд:
- JavaScript
- TypeScript
- Vue
- Vuex

### Бэкенд:
- Python (Flask)
- SQLAlchemy
- MySQL

### Другое:
- А также различные библиотеки для реализации авторизации/регистрации и создания компонентов (например графиков).

## ⚙️ Инструкция по запуску

### Локальный запуск

- Склонировать проект `git clone https://github.com/golosoman/GigaType.git`
- Установить **Python 3.12**, **MySQL 8**, **Node.js**
- Перейти в директорию проекта и выполнить команды:

  - В директории **backend**:

    ```bash
    python -m venv .venv
    .venv/Scripts/activate
    pip install -r requirements.txt
    alembic upgrade head
    python db_init.py
    python wsgi.py
    ```

  - В директории **frontend**:

    ```bash
    npm install
    npm run dev
    ```

- Приложение будет доступно по адресу: [http://localhost:5173](http://localhost:5173)

## 👨‍💻🔥👩‍💻 Над проектом работали

<table>
	<tr>
		<td align="left" valign="top">
			<a href="https://github.com/golosoman">
				<img src="https://avatars.githubusercontent.com/u/60601021?v=4" width="80" height="80" alt=""/>
				<br />
				<sub>🔧<b>Константин</b>🔧</sub>
			</a>
			<br />
			<sub>Team Lead</br>Frontend</br>Backend</sub>
		</td>
    <td align="left" valign="top">
			<a href="https://github.com/Mort3gar">
				<img src="https://avatars.githubusercontent.com/u/104523214?v=4" width="80" height="80" alt=""/>
				<br />
				<sub><b>Степан</b></sub>
			</a>
			<br />
			<sub>Backend</sub>
		</td>
    <td align="left" valign="top">
			<a href="https://github.com/aalexaashkaa">
				<img src="https://avatars.githubusercontent.com/u/157103630?v=4" width="80" height="80" alt=""/>
				<br />
				<sub><b>Александр</b></sub>
			</a>
			<br />
			<sub>Дизайнер</br>Тестировщик</sub>
		</td>
	</tr>
</table>
