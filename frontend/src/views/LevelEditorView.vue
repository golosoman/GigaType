<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор уровня</h2>
    <TableLevelEditor :headers="tableHeaders" :data="tableData" customStyle="margin: 20px; width: 500px"
        @addButtonClicked="openModal" />
    <CreateLevelWindow :isVisible="isModalVisible" @update:isVisible="isModalVisible = $event"></CreateLevelWindow>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NavigationBarForAdmin } from '@/component/trainer';
import { TableLevelEditor, CreateLevelWindow } from '@/component/trainer';

const isModalVisible = ref(false);

const openModal = () => {
    isModalVisible.value = true;
};

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