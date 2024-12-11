<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор упражнений</h2>
    <BaseDropdown v-model="selectedOption" :options="options" placeholder="Выберите уровень сложности" />
    <TableExerciseEditor :headers="tableHeaders" :data="tableData" customStyle="margin: 20px; width: 500px"
        @addButtonClicked="openModal" @exerciseClick="handleExerciseClick" />

    <CreateExerciseWindow :isVisible="isModalVisible" :keyboardZones="keyboardZones" :minCount="minCount"
        :maxCount="maxCount" :numberErrors="maxMistakes" :timePressKey="keyPressTime"
        :difficulty-id="selectedOption?.value" @update:isVisible="isModalVisible = $event" />

    <EditExerciseWindow :isVisible="isEditModalVisible" :keyboardZones="keyboardZones" :minCount="minCount"
        :maxCount="maxCount" :numberErrors="maxMistakes" :timePressKey="keyPressTime" :taskId="tableData[0]?.uid"
        :difficultyId="selectedOption?.value" :textExercise="currentExerciseContent"
        @update:isVisible="isEditModalVisible = $event" />
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { NavigationBarForAdmin, TableExerciseEditor, CreateExerciseWindow, EditExerciseWindow } from '@/component/trainer';
import { BaseDropdown } from '@/component/UI';
import { transformZones } from '@/component/Trainer/modalWindow';

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
    uid: string;
}

const isModalVisible = ref(false);
const isEditModalVisible = ref(false);
const currentExerciseContent = ref('');

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
    }
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

<style scoped></style>
