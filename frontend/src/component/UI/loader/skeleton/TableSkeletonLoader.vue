<template>
    <div class="skeleton-loader">
        <div class="skeleton-header">
            <div class="skeleton-cell header-cell"></div>
            <div class="skeleton-cell header-cell"></div>
        </div>
        <div class="skeleton-row" v-for="index in 5" :key="index">
            <div class="skeleton-cell"></div>
            <div class="skeleton-cell"></div>
        </div>
    </div>
</template>

<style scoped>
.skeleton-loader {
    display: flex;
    flex-direction: column;
    padding: 20px;
    /* Добавляем отступ для всего контейнера */
    background-color: #f9f9f9;
    /* Фоновый цвет для скелетона */
    border-radius: 8px;
    /* Скругление углов */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    /* Тень для эффекта глубины */
}

.skeleton-header {
    display: flex;
    /* Делаем заголовок флекс-контейнером */
    margin-bottom: 15px;
    /* Отступ снизу для заголовка */
}

.skeleton-header,
.skeleton-cell {
    background-color: #e0e0e0;
    border-radius: 4px;
    animation: pulse 1.5s infinite ease-in-out;
}

.skeleton-cell {
    flex: 1;
    height: 20px;
    margin: 5px;
    /* Отступ между ячейками */
}

/* Добавляем стиль для ячеек заголовка */
.header-cell {
    height: 25px;
    /* Высота ячеек заголовка больше */
    margin: 0 10px;
    /* Отступы для ячеек заголовка */
}

/* Стили для строк скелетона */
.skeleton-row {
    display: flex;
}

/* Анимация пульсации */
@keyframes pulse {
    0% {
        background-color: #e0e0e0;
    }

    50% {
        background-color: #d0d0d0;
        /* Цвет при пульсации */
    }

    100% {
        background-color: #e0e0e0;
    }
}
</style>

Найти еще