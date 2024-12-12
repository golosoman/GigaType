<template>
    <div class="modal-overlay" v-if="isVisible">
        <div class="modal">
            <div class="modal-header">
                <h1>Результаты</h1>
            </div>
            <div class="modal-body">
                <p><strong>Уровень:</strong> {{ levelName }}</p>
                <p><strong>Упражнение:</strong> {{ exerciseName }}</p>
                <p><strong>Скорость нажатий в минуту:</strong> {{ wpm }}</p>
                <p><strong>Количество допущенных ошибок:</strong> {{ errorsMade }}/{{ allowedErrors }}</p>
                <p><strong>Затраченное время:</strong> {{ timeSpent }} секунд</p>
                <p><strong>Счет:</strong> {{ score }}</p>
            </div>
            <div class="modal-footer">
                <BaseLink
                    customStyle="width: 160px; height: 40px; border-radius: 15px; font-size: 25px; color: #012E4A;"
                    href="#" @click.prevent="reloadPage">Повторить</BaseLink>
                <BaseLink customStyle="width: 200px; height: 40px;border-radius: 15px; font-size: 25px; color: #012E4A;"
                    href="/app/choose_exercise">К упражнениям</BaseLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import BaseLink from '@/component/UI/link/BaseLink.vue';
import { defineProps } from 'vue';

const props = defineProps<{
    isVisible: boolean; // Признак видимости модального окна
    levelName: string; // Название уровня
    exerciseName: string; // Название упражнения
    wpm: number; // Скорость нажатий в минуту
    errorsMade: number; // Количество допущенных ошибок
    allowedErrors: number; // Допустимое количество ошибок
    timeSpent: number; // Затраченное время в секундах
    score: number; // Счет
}>();

const reloadPage = () => {
    window.location.reload();
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 3;
}

.modal {
    background: #D9D9D9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
}

.modal-header {
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-body {
    margin: 20px 0;
}

.modal-footer {
    display: flex;
    justify-content: space-between;
}

.modal-link {
    color: blue;
    text-decoration: underline;
    cursor: pointer;
}
</style>
