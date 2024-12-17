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
                <div>
                    <BaseButton @click="handleImageUpload"
                        customStyle="width: 350px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
                        Изменить фотографию
                    </BaseButton>
                    <input type="file" @change="onFileChange" accept="image/*" />
                </div>
            </div> -->
            <div>
                <h1>Статистика</h1>
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
                        <RatingTable :userData="traineeData" custom-style="width: 500px"></RatingTable>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { NavigationBarForTrainee, RatingTable, LevelTable } from '@/component/Trainer';
import { BaseImage, BaseButton, BaseInputWithLabel, BaseDropdown } from '@/component/UI';
import UserImage from '@/assets/User.png';
import { ref, onMounted, watch } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js';
import { useUser } from '@/store'; // Импортируем store

const userImage = ref(UserImage); // Инициализация с изображением по умолчанию
const selectedFile = ref<File | null>(null); // Для хранения выбранного файла

// Функция для обработки изменения файла
const onFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        selectedFile.value = target.files[0];

        // Создаем временный URL для выбранного изображения
        userImage.value = URL.createObjectURL(selectedFile.value);
    }
};

// Функция для загрузки изображения на сервер
const handleImageUpload = async () => {
    if (!selectedFile.value) {
        console.error('Файл не выбран');
        return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile.value);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Ошибка при загрузке изображения');
        }

        const data = await response.json();
        userImage.value = data.imageUrl; // Предполагается, что сервер возвращает URL изображения
        console.log('Изображение загружено:', data.imageUrl);
    } catch (error) {
        console.error('Ошибка при загрузке изображения:', error);
    }
};


// Инициализация store
const userStore = useUser();

// interface DifficultyLevel {
//     name: string;
//     uid: string;
//     min_length: number;
//     max_length: number;
//     key_press_time: number;
//     max_mistakes: number;
//     zones: { keys: string; uid: string }[];
//     tasks: Task[];
// }
interface DifficultyLevel {
    name: string;
    uid: string;
}

// interface Task {
//     name: string;
//     content: string;
//     difficulty_id: string;
//     uid: string;
// }

interface SpeedData {
    clicks_per_minute: number;
    timestamp: string;
    uid: string;
}

interface UserStatisticsData {
    used_time: number;
    mistakes: number;
    clicks_number: number;
    success: boolean;
    score: number;
    clicks_per_minute: number;
    timestamp: string;
    max_mistakes: number;
    name: string;
}

interface TraineeData {
    login: string;
    scores: number;
}

// Функция для выхода из аккаунта
const handleLogout = async () => {
    try {
        await userStore.logout(); // Вызов метода logout из store
        // Дополнительные действия после выхода (например, перенаправление на главную страницу)
        window.location.href = '/'; // Перенаправление на главную страницу (или другую страницу)
    } catch (error) {
        console.error('Ошибка при выходе:', error);
    }
};

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

const options = ref<{ label: string; value: string }[]>([]);
const selectedOption = ref<{ label: string; value: string } | null>(null);

const chartData = ref({
    labels: [] as string[],
    datasets: [
        {
            label: 'Скорость ввода (симв/мин)',
            data: [] as number[],
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

const userName = ref(localStorage.getItem("login"));

const userStatistics = ref([] as any[]);
interface TraineeRanking {
    "Место": number;
    "Пользователь": string;
    "Рейтинг": number;
}

const traineeData = ref<TraineeRanking[]>([]);

// Функция для получения уровней сложности
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

// Функция для получения данных скорости
const fetchSpeedData = async () => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        console.error('User  ID not found in localStorage');
        return;
    }

    try {
        const response = await fetch(`/api/stat/get?user_uuid=${userId}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: SpeedData[] = await response.json();

        // Преобразование данных для графика
        chartData.value.labels = data.map(item => item.timestamp);
        chartData.value.datasets[0].data = data.map(item => item.clicks_per_minute);

    } catch (error) {
        console.error('Ошибка при получении данных скорости:', error);
    }
};

// Функция для получения статистики по уровням
const fetchUserStatistics = async () => {
    const userId = localStorage.getItem('userId');
    if (!userId || !selectedOption.value) {
        console.error('User  ID or selected difficulty not found');
        return;
    }

    try {
        const response = await fetch(`/api/stat/get?difficulty_uid=${selectedOption.value.value}&user_uuid=${userId}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: UserStatisticsData[] = await response.json();

        // Преобразование данных для таблицы
        userStatistics.value = data.map(item => ({
            "Упражнение": item.name,
            "Статус": item.success ? 'Выполнено' : 'Не выполнено',
            "Скорость": `${item.clicks_per_minute} симв/мин`,
            "Ошибки": `${item.mistakes}/${item.max_mistakes}`,
            "Время": `${item.used_time} с`,
            "Дата": `${item.timestamp}`
        }));

    } catch (error) {
        console.error('Ошибка при получении статистики по уровням:', error);
    }
};

// Функция для получения рейтинга среди обучаемых
const fetchTraineeData = async () => {
    try {
        const response = await fetch('/api/stat/top');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: TraineeData[] = await response.json();

        // Преобразование данных для таблицы
        traineeData.value = data.map((item, index) => ({
            "Место": index + 1,
            "Пользователь": item.login,
            "Рейтинг": item.scores,
        }));

    } catch (error) {
        console.error('Ошибка при получении данных рейтинга:', error);
    }
};

// Вызов функций при монтировании компонента
onMounted(() => {
    fetchDifficultyLevels();
    fetchSpeedData();
    fetchTraineeData(); // Добавлено для получения данных рейтинга
});

// Следим за изменением выбранного уровня сложности и загружаем данные
watch(selectedOption, () => {
    fetchUserStatistics();
});

// Reactive property to track which tab is active
const activeTab = ref('');

// Function to set the active tab
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