<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор уровня</h2>
    <TableLevelEditor :headers="tableHeaders" :data="tableData" customStyle="margin: 20px; width: 500px"
        @createButtonClick="openModal" @levelClick="handleLevelClick" />
    <CreateLevelWindow :isVisible="isModalVisible" @update:isVisible="isModalVisible = $event"></CreateLevelWindow>
    <EditLevelWindow :isVisible="isEditModalVisible" :keyboardZones="selectedLevelData.zones"
        :minCount="selectedLevelData.min_length" :maxCount="selectedLevelData.max_length"
        :maxErrors="selectedLevelData.max_mistakes" :timePressKey="selectedLevelData.key_press_time"
        :uid="selectedLevelData.uid" @update:isVisible="isEditModalVisible = $event" v-if="isEditModalVisible">
    </EditLevelWindow>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { NavigationBarForAdmin } from '@/component/trainer';
import { TableLevelEditor, CreateLevelWindow, EditLevelWindow } from '@/component/trainer';

const isModalVisible = ref(false);
const isEditModalVisible = ref(false); // Новая переменная для управления видимостью модального окна редактирования
const selectedLevelUid = ref<string | null>(null);
const selectedLevelData = ref<any>(null); // Данные уровня сложности
const tableHeaders = ['Уровень', 'Название']; // Заголовки таблицы
const tableData = ref<{ level: number; name: string; uid: string }[]>([]); // Динамические данные таблицы

const openModal = () => {
    isModalVisible.value = true;
};

// Метод для загрузки данных с сервера
const fetchLevels = async () => {
    try {
        const response = await axios.get('/api/difficulty/get', { withCredentials: true });
        // Фильтруем данные, чтобы использовать только те уровни, которые имеют подлинные значения
        tableData.value = response.data
            .filter((level: any) => level.name) // Убираем уровни без имени
            .map((level: any) => ({
                level: level.name, // Используем поле name как уровень
                name: level.name, // Используем поле name для отображения
                uid: level.uid // Добавляем uid
            }));
    } catch (error) {
        console.error('Ошибка при загрузке уровней:', error);
    }
};

// Обработчик клика на уровень
const handleLevelClick = async (uid: string) => {
    selectedLevelUid.value = uid;
    console.log('UID уровня:', uid); // Лог для проверки
    await fetchLevelData(uid); // Запрашиваем данные уровня по uid
};

// Метод для получения данных уровня по uid
const fetchLevelData = async (uid: string) => {
    try {
        const response = await axios.get(`/api/difficulty/get?uid=${uid}`, { withCredentials: true });
        selectedLevelData.value = response.data[0]; // Предполагаем, что данные приходят в виде массива
        console.log('Данные уровня:', selectedLevelData.value); // Лог для проверки
        isEditModalVisible.value = true; // Открываем модальное окно редактирования
    } catch (error) {
        console.error('Ошибка при загрузке данных уровня:', error);
    }
};

// Вызываем fetchLevels при монтировании компонента
onMounted(() => {
    fetchLevels();
});
</script>

<style scoped></style>