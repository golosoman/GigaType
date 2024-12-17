<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h1>Редактор уровня</h1>
    <div v-if="isLoading">
        <SpinLoader v-if="isLoading"></SpinLoader>
    </div>
    <TableLevelEditor v-else :headers="tableHeaders" :data="tableData" customStyle="margin: 20px; width: 500px"
        @createButtonClick="openModal" @levelClick="handleLevelClick" />
    <CreateLevelWindow @show-error="showToast" @level-added="handleLevelAdd" :isVisible="isModalVisible"
        @update:isVisible="isModalVisible = $event">
    </CreateLevelWindow>
    <EditLevelWindow @show-error="showToast" :isVisible="isEditModalVisible" :keyboardZones="selectedLevelData.zones"
        :difficulty-id="selectedLevelUid" :minCount="selectedLevelData.min_length"
        :maxCount="selectedLevelData.max_length" :maxErrors="selectedLevelData.max_mistakes"
        :timePressKey="selectedLevelData.key_press_time" :uid="selectedLevelData.uid"
        @update:isVisible="isEditModalVisible = $event" v-if="isEditModalVisible">
    </EditLevelWindow>
    <Toast v-if="toastVisible" v-model="toastVisible" :message="toastMessage" type="error"
        @close="toastVisible = false" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { TableLevelEditor, CreateLevelWindow, EditLevelWindow, NavigationBarForAdmin } from '@/component/Trainer';
import { Toast, SpinLoader } from '@/component/UI';
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

const isModalVisible = ref(false);
const isEditModalVisible = ref(false); // Новая переменная для управления видимостью модального окна редактирования
const selectedLevelUid = ref<string | undefined>(undefined); // Изменено на string | undefined
const selectedLevelData = ref<any>(null); // Данные уровня сложности
const tableHeaders = ['Уровень', 'Название']; // Заголовки таблицы
const tableData = ref<{ level: number; name: string; uid: string }[]>([]); // Динамические данные таблицы

const openModal = () => {
    isModalVisible.value = true;
};

const handleLevelAdd = (newLevel: { name: string; level: number; uid: string }) => {
    console.log(`handleLevelAdd ${JSON.stringify(newLevel)}`);
    tableData.value.push(newLevel);

    // Сортируем массив по полю level
    tableData.value.sort((a, b) => a.level - b.level);
}

// Метод для загрузки данных с сервера
const fetchLevels = async () => {
    isLoading.value = true; // Начинаем загрузку
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
    } finally {
        isLoading.value = false;
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

<style scoped>
h1 {
    margin-left: 15px;
    color: #012e4a;
    font-family: "Alegreya Sans SC";
}
</style>