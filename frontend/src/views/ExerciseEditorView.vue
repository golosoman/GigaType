<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h1>Редактор упражнений</h1>
    <BaseDropdown custom-style="margin-left: 15px;" v-model="selectedOption" :options="options"
        placeholder="Выберите уровень сложности" />
    <div v-if="isLoading">
        <SpinLoader v-if="isLoading"></SpinLoader>
    </div>
    <TableExerciseEditor v-else :headers="tableHeaders" :data="tableData" customStyle="margin: 20px; width: 500px"
        :isLoading="isLoading" @addButtonClicked="openModal" @exerciseClick="handleExerciseClick" />

    <CreateExerciseWindow @show-error="showToast" @exercise-added="handleExerciseAdded" :isVisible="isModalVisible"
        :keyboardZones="keyboardZones" :minCount="minCount" :maxCount="maxCount" :numberErrors="maxMistakes"
        :timePressKey="keyPressTime" :difficulty-id="selectedOption?.value"
        @update:isVisible="isModalVisible = $event" />

    <EditExerciseWindow @show-error="showToast" :isVisible="isEditModalVisible" :keyboardZones="keyboardZones"
        :keyboardZonesForTask="zonesTask" :minCount="minCount" :maxCount="maxCount" :numberErrors="maxMistakes"
        :timePressKey="keyPressTime" :taskId="uidTask" :difficultyId="selectedOption?.value"
        :textExercise="currentExerciseContent" @update:isVisible="isEditModalVisible = $event" />
    <Toast v-if="toastVisible" v-model="toastVisible" :message="toastMessage" type="error"
        @close="toastVisible = false" />
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { NavigationBarForAdmin, TableExerciseEditor, CreateExerciseWindow, EditExerciseWindow, transformZones } from '@/component/Trainer';
import { BaseDropdown, SpinLoader } from '@/component/UI';

import { Toast } from '@/component/UI';
const isLoading = ref(true); // Состояние загрузки
const toastVisible = ref(false)
const toastMessage = ref('')

const showToast = (message: string) => {
    toastMessage.value = message;
    toastVisible.value = true;
    setTimeout(() => {
        toastVisible.value = false;
    }, 3000);
}

interface DifficultyLevel {
    name: string;
    uid: string;
    min_length: number;
    max_length: number;
    key_press_time: number;
    max_mistakes: number;
    zones: { keys: string; uid: string }[];
    tasks: Task[];
}

interface Task {
    name: string;
    content: string;
    difficulty_id: string;
    zones: { keys: string; uid: string }[];
    uid: string;
}

const isModalVisible = ref(false);
const isEditModalVisible = ref(false);
const currentExerciseContent = ref('');
const zonesTask = ref([])
const uidTask = ref('')

const options = ref<{ label: string; value: string }[]>([]);
const selectedOption = ref<{ label: string; value: string } | null>(null);
const levels = ref<DifficultyLevel[]>([]);
const tableData = ref<{ name: string; value: string; level: string, uid: string; }[]>([]);

const openModal = () => {
    isModalVisible.value = true;
};

const minCount = ref(30);
const maxCount = ref(80);
const keyPressTime = ref(1.5);
const maxMistakes = ref(5);

const keyboardZones = ref<string[]>([]);

const tableHeaders = ['Уровень', 'Название'];

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

        levels.value = data;

    } catch (error) {
        console.error('Ошибка при получении уровней сложности:', error);
    }
};

const fetchTasksForSelectedLevel = async (uid: string) => {
    isLoading.value = true; // Начинаем загрузку
    try {
        const response = await fetch(`/api/difficulty/get?uid=${uid}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: DifficultyLevel[] = await response.json();

        const selectedLevel = data[0]; // Предполагаем, что вернется только один уровень

        if (selectedLevel) {
            minCount.value = selectedLevel.min_length;
            maxCount.value = selectedLevel.max_length;
            keyPressTime.value = selectedLevel.key_press_time;
            maxMistakes.value = selectedLevel.max_mistakes;
            keyboardZones.value = transformZones(selectedLevel.zones);

            tableData.value = selectedLevel.tasks.map(task => ({
                name: `Упражнение ${task.name}`,
                value: task.name,
                level: selectedLevel.name,
                uid: task.uid
            }));
        }
    } catch (error) {
        console.error('Ошибка при получении задач для уровня сложности:', error);
    } finally {
        isLoading.value = false; // Завершаем загрузку
    }
};

const handleExerciseAdded = (newExercise: { name: string; value: string; level: string; uid: string }) => {
    console.log(newExercise)
    tableData.value.push(newExercise); // Добавляем новый элемент в массив tableData
};


const handleExerciseClick = async (uid: string) => {
    try {
        const response = await fetch(`/api/task/get?uid=${uid}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        if (data.length > 0) {
            const exercise = data[0];
            currentExerciseContent.value = exercise.content; // Содержимое упражнения
            zonesTask.value = exercise.zones;
            uidTask.value = exercise.uid;
            // Установить другие свойства, если необходимо
            isEditModalVisible.value = true; // Открыть модальное окно редактирования
        }
    } catch (error) {
        console.error('Ошибка при получении упражнения:', error);
    }
};

watch(selectedOption, (newValue) => {
    if (newValue) {
        selectedOption.value = newValue
        console.log('Выбранный уровень:', newValue);
        fetchTasksForSelectedLevel(newValue.value);
        console.log(`${minCount.value} ${maxCount.value} ${keyPressTime.value} ${maxMistakes.value} ${keyboardZones.value} ${keyPressTime.value}`);
    }
});

onMounted(() => {
    fetchDifficultyLevels();
});
</script>

<style scoped>
h1 {
    margin-left: 15px;
    color: #012e4a;
    font-family: "Alegreya Sans SC";
}
</style>
