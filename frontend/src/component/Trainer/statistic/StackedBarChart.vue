<template>
    <BarChart :data="chartData" :options="chartOptions" :height="height" :width="width" />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default defineComponent({
    components: {
        BarChart: Bar,
    },
    data() {
        return {
            height: 400,
            width: 600,
            chartData: {
                labels: ['Упражнение 1', 'Упражнение 2', 'Упражнение 3'],
                datasets: [
                    {
                        label: 'Верные решения',
                        data: [15, 20, 10], // Количество верных решений для каждого упражнения
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    },
                    {
                        label: 'Ошибочные решения',
                        data: [5, 10, 15], // Количество ошибочных решений для каждого упражнения
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    },
                ],
            },
            chartOptions: {
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
            },
        };
    },
});
</script>