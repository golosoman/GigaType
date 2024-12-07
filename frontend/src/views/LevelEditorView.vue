<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор уровня</h2>
    <TableLevelEditor :headers="tableHeaders" :data="tableData" customStyle="margin: 20px; width: 500px"
        @addButtonClicked="openModal" />
    <CreateLevelWindow :isVisible="isModalVisible" @update:isVisible="isModalVisible = $event"></CreateLevelWindow>
    <!-- <EditLevelWindow></EditLevelWindow> -->
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { NavigationBarForAdmin } from '@/component/trainer';
import { TableLevelEditor, CreateLevelWindow } from '@/component/trainer';

const isModalVisible = ref(false);
const tableHeaders = ['Уровень', 'Название']; // Заголовки таблицы
const tableData = ref<{ level: number; name: string }[]>([]); // Динамические данные таблицы

const openModal = () => {
    isModalVisible.value = true;
};

// Метод для загрузки данных с сервера
const fetchLevels = async () => {
    try {
        const response = await axios.get('/api/difficulty/get', { withCredentials: true });
        // Преобразуем полученные данные для таблицы
        tableData.value = response.data.map((level: any, index: number) => ({
            level: index + 1, // Уровень можно определить по индексу
            name: level.name // Используем поле name из ответа
        }));
    } catch (error) {
        console.error('Ошибка при загрузке уровней:', error);
    }
};

// Вызываем fetchLevels при монтировании компонента
onMounted(() => {
    fetchLevels();
});
</script>

<style scoped></style>
