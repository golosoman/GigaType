<template>
    <div class="content">
        <NavigationBarForTrainee></NavigationBarForTrainee>
        <div>
            <div>
                <h1>
                    Выбрать список упражнений
                </h1>
                <BaseDropdown v-model="selectedOption" :options="options" placeholder="Выберите уровень сложности" />
            </div>
            <div>
                <h2>Таблица Упражнений</h2>
                <SpinLoader v-if="isLoading"></SpinLoader>
                <TableExercise v-else :headers="headers" :data="tableData" custom-style="width: 600px;" />
            </div>

        </div>
    </div>
</template>


<script setup lang="ts">
import { NavigationBarForTrainee, TableExercise } from '@/component/Trainer';
import { BaseDropdown, SpinLoader } from '@/component/UI';
import { ref, onMounted, watch } from 'vue'
const isLoading = ref(true); // Состояние загрузки


interface DifficultyLevel {
    name: string;
    uid: string;
    tasks: Task[];
}

interface Task {
    name: string;
    content: string;
    difficulty_id: string;
    uid: string;
}

const options = ref<{ label: string; value: string }[]>([]);
const selectedOption = ref<{ label: string; value: string } | null>(null);
const tableData = ref<{ name: string; exercise: string; level: string, taskId: string; levelId: string; }[]>([]);
const levels = ref<DifficultyLevel[]>([]);
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
    isLoading.value = true;
    try {
        const response = await fetch(`/api/difficulty/get?uid=${uid}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data: DifficultyLevel[] = await response.json();

        const selectedLevel = data[0]; // Предполагаем, что вернется только один уровень

        if (selectedLevel) {
            tableData.value = selectedLevel.tasks.map(task => ({
                name: `Упражнение ${task.name}`,
                exercise: task.name,
                level: selectedLevel.name,
                taskId: task.uid,
                levelId: uid
            }));
        }

    } catch (error) {
        console.error('Ошибка при получении задач для уровня сложности:', error);
    } finally {
        isLoading.value = false;
    }
};

watch(selectedOption, (newValue) => {
    if (newValue) {
        selectedOption.value = newValue
        console.log('Выбранный уровень:', newValue);
        fetchTasksForSelectedLevel(newValue.value);
    }
});

onMounted(() => {
    fetchDifficultyLevels();
});

const headers = ['Упражнение', 'Название'];

</script>

<style scoped>
.content {
    color: #012e4a;
    margin-left: 15px;
}
</style>