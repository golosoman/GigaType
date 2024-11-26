<template>
    <div class="content">
        <NavigationBarForTrainee></NavigationBarForTrainee>
        <div style="margin-left: 60px;">
            <div class="container">
                <div>
                    <BaseImage :src="UserImage"
                        customStyle="background-color: #81BECE; border-radius: 30px; width: 300px; height: 300px; margin-top: 40px;">
                    </BaseImage>
                </div>

                <div class="input-container">
                    <BaseInputWithLabel v-model="userName" label="Пользователь"
                        customStyleForInput="width: 450px; height: 57px; font-size: 32px; pointer-events: none;"
                        customStyleForLabel="font-size: 32px; pointer-events: none;">
                    </BaseInputWithLabel>
                </div>

            </div>
            <div>
                <BaseButton
                    customStyle="width: 35s0px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
                    Изменить фотографию
                </BaseButton>
            </div>
            <div>
                <h2>Статистика</h2>
                <div>
                    <BaseButton @click="setActiveTab('speed')"
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A;">
                        Скорость
                    </BaseButton>
                    <BaseButton @click="setActiveTab('levels')"
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A; margin-left: 20px;">
                        Уровни
                    </BaseButton>
                    <BaseButton @click="setActiveTab('trainees')"
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A; margin-left: 20px;">
                        Обучаемые
                    </BaseButton>
                </div>
                <div>
                    <div v-if="activeTab === 'speed'" style="width: 800px;">
                        <h2>Количество символов</h2>
                        <Line :data="chartData" :options="chartOptions" />
                    </div>
                    <div v-else-if="activeTab === 'levels'">
                        <h2>Статистика по уровням</h2>
                        <BaseDropdown v-model="selectedOption" :options="options"
                            placeholder="Выберите уровень сложности" />
                        <LevelTable :tableData="userStatistics" customStyle="width: 600px; margin-top: 10px;" />
                    </div>
                    <div v-else-if="activeTab === 'trainees'">
                        <h2>Рейтинг среди обучаемых</h2>
                        <RatingTable :user-data="userData" custom-style="width: 500px"></RatingTable>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { NavigationBarForTrainee, RatingTable, LevelTable } from '@/component/trainer';
import { BaseImage, BaseButton, BaseInputWithLabel, BaseDropdown } from '@/component/UI';
import UserImage from '@/assets/User.png'
import { ref } from 'vue'

import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

const options = ['Уровень 1', 'Уровень 2', 'Уровень 3']; // Опции для выпадающего списка
const selectedOption = ref(null); // Двусторонняя привязка с опциями

const chartData = ref({
    labels: [
        '2023-10-01 10:00',
        '2023-10-01 11:00',
        '2023-10-01 12:00',
        '2023-10-01 13:00',
        '2023-10-01 14:00',
        '2023-10-02 10:00',
        '2023-10-02 11:00',
        '2023-10-02 12:00',
        '2023-10-02 13:00',
        '2023-10-02 14:00',
        '2023-10-03 10:00',
        '2023-10-03 11:00',
    ],
    datasets: [
        {
            label: 'Скорость ввода (симв/мин)',
            data: [100, 150, 120, 130, 160, 140, 170, 180, 190, 200, 210, 220],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
        },
    ],
});

const chartOptions = ref({
    responsive: true,
    plugins: {
        legend: {
            position: 'top' as const,
        },
        title: {
            display: true,
            text: 'Статистика скорости ввода',
        },
    },
});

const userName = ref('trainee')

const userData = ref([
    { Место: 1, Пользователь: 'Ivan', Рейтинг: 1500 },
    { Место: 2, Пользователь: 'Anna', Рейтинг: 1450 },
    { Место: 3, Пользователь: 'Petr', Рейтинг: 1400 },
    { Место: 4, Пользователь: 'Svetlana', Рейтинг: 1350 },
    { Место: 5, Пользователь: 'Dmitry', Рейтинг: 1300 },
]);

const userStatistics = ref([
    { Упражнение: 1, Статус: 'Выполнено', Скорость: '110 симв/мин', Ошибки: '3/5', Время: '120 с' },
    { Упражнение: 2, Статус: 'Не выполнено', Скорость: '130 симв/мин', Ошибки: '5/6', Время: '130 с' },
    { Упражнение: 3, Статус: 'Выполнено', Скорость: '120 симв/мин', Ошибки: '5/5', Время: '125 с' },
    // Добавьте дополнительные данные по мере необходимости
]);

// Reactive property to track which tab is active
const activeTab = ref('');

// Function to set the active tab
const setActiveTab = (tab: string) => {
    activeTab.value = tab;
};
</script>

<style scoped>
.content {
    display: flex;
    flex-direction: column;
}

.container {
    display: flex;
    align-items: flex-start;
    margin-top: 20px;
}

.input-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 50px;
    margin-top: 50px;
}

.BaseImage {
    margin-top: 40px;
}
</style>