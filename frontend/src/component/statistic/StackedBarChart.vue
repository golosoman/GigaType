<template>
    <div>
        <Bar ref="chart" />
    </div>
</template>

<script>
import { Bar } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

// Регистрация необходимых компонентов Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
    extends: Bar,
    name: "StackedBarChart",
    props: {
        data: {
            type: Array,
            required: true
        }
    },
    mounted() {
        // Проверяем, что данные существуют и являются массивом
        if (!Array.isArray(this.data) || this.data.length === 0) {
            console.error("Данные не переданы или пусты");
            return; // Выходим из метода, если данные недоступны
        }

        const chartData = {
            labels: [],
            datasets: [
                {
                    label: "New",
                    backgroundColor: "#f87979",
                    data: []
                },
                {
                    label: "Old",
                    backgroundColor: "#c0c0c0",
                    data: []
                }
            ]
        };

        // Заполняем данные
        for (let i = 0; i < this.data.length; i++) {
            chartData.labels.push(this.data[i].date);
            chartData.datasets[0].data.push(this.data[i].new);
            chartData.datasets[1].data.push(this.data[i].old);
        }

        // Рендерим график с подготовленными данными и опциями
        this.renderChart(chartData, {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true // Устанавливаем наложение по оси X
                },
                y: {
                    stacked: true // Устанавливаем наложение по оси Y
                }
            }
        });
    }
};
</script>


<style scoped>
/* Добавьте стили, если необходимо */
</style>

Найти еще