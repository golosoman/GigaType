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
                    <BaseInputWithLabel v-model="userName!" label="Пользователь"
                        customStyleForInput="width: 450px; height: 57px; font-size: 32px; pointer-events: none;"
                        customStyleForLabel="font-size: 32px; pointer-events: none;">
                    </BaseInputWithLabel>
                </div>
                <!-- Кнопка "Выход" -->
                <div class="logout-button-container">
                    <BaseButton @click="handleLogout"
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; background-color: #FF8080; margin-left: 10px;">
                        Выход
                    </BaseButton>
                </div>
            </div>
            <!-- <div>
                <BaseButton
                    customStyle="width: 350px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
                    Изменить фотографию
                </BaseButton>
            </div> -->
            <div>
                <h1>Статистика</h1>
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
                            <Bar v-model:data="chartData" v-model:options="chartOptions" />
                        </div>
                    </div>
                    <div v-else-if="activeTab === 'trainees'">
                        <h2>Рейтинг среди обучаемых</h2>
                        <RatingTable :userData="traineeData" custom-style="width: 500px"></RatingTable>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, type Ref } from 'vue';
import { NavigationBarForAdmin, RatingTable } from '@/component/Trainer';
import { BaseImage, BaseButton, BaseInputWithLabel, BaseDropdown } from '@/component/UI';
import UserImage from '@/assets/User.png';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { useUser } from '@/store'; // Импортируем store

// Инициализация store
const userStore = useUser();



interface DifficultyLevel {
    name: string;
    uid: string;
}

interface TraineeData {
    login: string;
    scores: number;
}

interface TraineeRanking {
    Место: number;
    Пользователь: string;
    Рейтинг: number;
}

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const options = ref<{ label: string; value: string }[]>([]);
const selectedOption = ref<{ label: string; value: string } | null>(null);
// Определяем тип данных, которые вы получаете
interface ExerciseData {
    attempts: number[]; // Массив чисел
    name: string;       // Имя упражнения
}

// Функция для выхода из аккаунта
const handleLogout = async () => {
    try {
        await userStore.logout(); // Вызов метода logout из store
        window.location.href = '/'; // Перенаправление на главную страницу (или другую страницу)
    } catch (error) {
        console.error('Ошибка при выходе:', error);
    }
};

// Определяем тип для данных гистограммы
interface ChartData {
    labels: string[];
    datasets: {
        label: string;
        data: number[]; // Предполагаем, что данные будут числовыми
        backgroundColor: string;
    }[];
}

// Явно указываем тип для chartData
const chartData: Ref<ChartData> = ref({
    labels: [],
    datasets: [
        {
            label: 'Верные решения',
            data: [],
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
        {
            label: 'Ошибочные решения',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
        },
    ],
});
const chartOptions = ref({
    responsive: true,
    scales: {
        x: {
            stacked: true,
        },
        y: {
            stacked: true,
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
});

const userName = ref(localStorage.getItem("login"));
const traineeData = ref<TraineeRanking[]>([]);

const fetchDifficultyLevels = async () => {
    try {
        const response = await fetch('/api/difficulty/get');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: DifficultyLevel[] = await response.json();

        options.value = data.map(item => ({
            label: `Уровень ${item.name}`,
            value: item.uid,
        }));

        if (options.value.length > 0) {
            selectedOption.value = options.value[0];
        }
    } catch (error) {
        console.error('Ошибка при получении уровней сложности:', error);
    }
};

const fetchTraineeData = async () => {
    try {
        const response = await fetch('/api/stat/top');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: TraineeData[] = await response.json();

        traineeData.value = data.map((item, index) => ({
            Место: index + 1,
            Пользователь: item.login,
            Рейтинг: item.scores,
        }));
    } catch (error) {
        console.error('Ошибка при получении данных рейтинга:', error);
    }
};

// Функция для получения данных по упражнениям
const fetchExerciseData = async (difficultyUid: string) => {
    try {
        const response = await fetch(`/api/stat/get?difficulty_uid=${difficultyUid}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: ExerciseData[] = await response.json();

        console.log('Полученные данные:', data); // Проверка полученных данных

        // Проверка, есть ли данные, и обновление данных для гистограммы
        if (data.length > 0) {
            chartData.value = {
                labels: data.map((item: ExerciseData) => `Упражнение ${item.name}`),
                datasets: [
                    {
                        label: 'Верные решения',
                        data: data.map((item: ExerciseData) => item.attempts[0]),
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    },
                    {
                        label: 'Ошибочные решения',
                        data: data.map((item: ExerciseData) => item.attempts[1]),
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    },
                ],
            };
        } else {
            // Если данных нет, обнуляем массивы
            chartData.value = {
                labels: [],
                datasets: [
                    {
                        label: 'Верные решения',
                        data: [0],
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    },
                    {
                        label: 'Ошибочные решения',
                        data: [0],
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    },
                ],
            };
        }
    } catch (error) {
        console.error('Ошибка при получении данных по упражнениям:', error);
    }
};

// Вызов функций при монтировании компонента
onMounted(() => {
    fetchDifficultyLevels();
    fetchTraineeData();
});

// Следим за изменением выбранного уровня сложности
watch(selectedOption, (newValue) => {
    if (newValue) {
        fetchExerciseData(newValue.value); // Передаем uid уровня сложности
    }
});

const activeTab = ref('');
const setActiveTab = (tab: string) => {
    activeTab.value = tab;
};
</script>

<style scoped>
h1 {
    color: #012e4a;
}

h2 {
    color: #012e4a;
}

.content {
    display: flex;
    flex-direction: column;
}

.container {
    display: flex;
    align-items: flex-start;
    margin-top: 20px;
    justify-content: space-between;
    /* Добавлено для выравнивания по краям */
}

.input-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 50px;
    margin-top: 50px;
}

.logout-button-container {
    display: flex;
    align-items: center;
    margin-left: auto;
    /* Выровнять кнопку по правому краю */
    margin-top: 50px;
    /* Добавить отступ сверху для выравнивания */
}

.BaseImage {
    margin-top: 40px;
}
</style>