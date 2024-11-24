<template>
    <div class="content">
        <NavigationBarForTrainee></NavigationBarForTrainee>
        <div>
            <div>
                <h2>
                    Выбрать список упражнений.
                </h2>
                <BaseDropdown v-model="selectedOption" :options="options" placeholder="Выберите уровень сложности" />
            </div>
            <div>
                <h2>Таблица Упражнений</h2>
                <TableExercise :headers="headers" :data="exerciseData" />
            </div>

        </div>
    </div>
</template>


<script setup lang="ts">
import { NavigationBarForTrainee, TableExercise } from '@/component/trainer';
import { BaseDropdown } from '@/component/UI';
import { ref } from 'vue'

const options = ['Уровень 1', 'Уровень 2', 'Уровень 3']; // Опции для выпадающего списка
const selectedOption = ref(null); // Двусторонняя привязка с опциями

const headers = ['Упражнение', 'Название'];
const exerciseData = ref([
    { exercise: 'Упражнение 1', level: 1, number: 1 },
    { exercise: 'Упражнение 2', level: 1, number: 2 },
    { exercise: 'Упражнение 3', level: 1, number: 3 },
    // Добавьте дополнительные данные по мере необходимости
]);
</script>

<style scoped></style>