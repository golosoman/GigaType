<template>
    <div class="content">
        <NavigationBarForAdmin></NavigationBarForAdmin>
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
                <StackedBarChart></StackedBarChart>
            </div>
            <div>
                <h2>Статистика</h2>
                <div>
                    <BaseButton @click="setActiveTab('exercise')"
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A; margin-left: 20px;">
                        Упражнения
                    </BaseButton>
                    <BaseButton @click="setActiveTab('trainees')"
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A; margin-left: 20px;">
                        Обучаемые
                    </BaseButton>
                </div>
                <div>
                    <div v-if="activeTab === 'exercise'">
                        <h2>Статистика по упражнениям</h2>
                        <BaseDropdown v-model="selectedOption" :options="options"
                            placeholder="Выберите уровень сложности" />
                        <div style="width: 600px; height: 300px;">
                            <Bar :data="chartData" :options="chartOptions" />
                        </div>
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
import { NavigationBarForAdmin, RatingTable } from '@/component/trainer';
import { BaseImage, BaseButton, BaseInputWithLabel, BaseDropdown } from '@/component/UI';
import UserImage from '@/assets/User.png'
import { ref } from 'vue'
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const options = ['Уровень 1', 'Уровень 2', 'Уровень 3']; // Опции для выпадающего списка
const selectedOption = ref(null); // Двусторонняя привязка с опциями

const chartData = ref({
    labels: ['Упражнение 1', 'Упражнение 2', 'Упражнение 3'],
    datasets: [
        {
            label: 'Верные решения',
            data: [15, 20, 0], // Количество верных решений для каждого упражнения
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
        {
            label: 'Ошибочные решения',
            data: [5, 10, 0], // Количество ошибочных решений для каждого упражнения
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
        },
    ],
})
const chartOptions = ref({
    responsive: true,
    scales: {
        x: {
            stacked: true, // Включаем накопление по оси X
        },
        y: {
            stacked: true, // Включаем накопление по оси Y
            beginAtZero: true,
        },
    },
    plugins: {
        legend: {
            position: 'top' as const,
        },
        title: {
            display: true,
            text: 'Накопительная диаграмма верных и ошибочных решений',
        },
    },
})



const userName = ref('admin')

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