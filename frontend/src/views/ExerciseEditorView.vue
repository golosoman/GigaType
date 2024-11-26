<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор упражнений</h2>
    <TableExerciseEditor :headers="tableHeaders" :data="tableData" customStyle="margin: 20px; width: 500px">
    </TableExerciseEditor>
</template>

<script setup lang="ts">
import { NavigationBarForAdmin, TableExerciseEditor } from '@/component/trainer';
const tableHeaders = ['Уровень', 'Название']; // Заголовки таблицы

const tableData = [
    { name: 'Упражнение 1', value: 10, level: 1, number: 1 },
    { name: 'Упражнение 2', value: 20, level: 1, number: 2 },
    { name: 'Упражнение 3', value: 30, level: 2, number: 1 },
    { name: 'Упражнение 4', value: 40, level: 2, number: 2 },
    { name: 'Упражнение 5', value: 50, level: 3, number: 1 },
];
</script>

<style scoped></style>