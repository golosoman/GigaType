<template>
    <div class="container">
        <div class="developer-info">
            <h1>Сведения о разработчиках</h1>
            <div class="university-info">
                <p>Самарский университет</p>
                <p>Кафедра программных систем</p>
                <p>Курсовой проект по дисциплине “Программная инженерия”</p>
                <p>Тема проекта “Клавиатурный тренажер” с функциями администратора</p>
            </div>
            <h2>Разработчики (обучающиеся группы 6403-020302D)</h2>
            <ul class="developers-list">
                <li>Лапин К.С.</li>
                <li>Петров А.И.</li>
                <li>Марковский С.А.</li>
            </ul>
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
    /* Цвет фона для контраста */
}

.developer-info {
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

.university-info {
    margin-bottom: 20px;
}

.developers-list {
    list-style-type: none;
    padding: 0;
}

.developers-list li {
    margin: 5px 0;
}

.footer {
    text-align: center;
    margin-top: 20px;
    font-weight: bold;
}
</style>

Найти еще