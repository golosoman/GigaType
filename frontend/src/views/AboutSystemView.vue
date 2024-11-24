<template>
    <div class="container">
        <div class="system-info">
            <h1>Сведения о системе</h1>
            <h2>Клавиатурный тренажер</h2>
            <div class="description">
                <p>
                    Клавиатурный тренажер предназначен для обучения пользователей
                    слепой печати на клавиатуре. Система предлагает различные режимы
                    тренировки и позволяет отслеживать прогресс пользователя.
                </p>
            </div>
            <h3>Основные функции</h3>
            <ul class="features-list">
                <li>Обучение слепой печати с использованием различных текстов.</li>
                <li>Статистика и анализ результатов тренировок.</li>
                <li>Возможность выбора уровня сложности.</li>
                <li>Функции администратора для управления пользователями.</li>
            </ul>
            <h3>Технологии</h3>
            <p>
                Система разработана с использованием современных веб-технологий:
                HTML, CSS, JavaScript и фреймворка Vue.js, что обеспечивает
                интерактивность и удобство использования.
            </p>
            <p class="footer">Самара 2024</p>
        </div>
    </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* Занять всю высоту экрана */
    background-color: #f0f0f0;
    /* Цвет фона для контраста */
}

.system-info {
    max-width: 600px;
    margin: 20px;
    padding: 20px;
    border: 1px solid #012E4A;
    border-radius: 8px;
    background-color: #ffffff;
    /* Цвет фона карточки */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #012E4A;
}

.description {
    margin-bottom: 20px;
}

.features-list {
    list-style-type: disc;
    /* Используем маркеры для списка */
    padding-left: 20px;
    /* Отступ для списка */
}

.footer {
    text-align: center;
    margin-top: 20px;
    font-weight: bold;
}
</style>
