<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор пользователей</h2>
    <TableUserEdit :headers="headers" v-model:data="users" customStyle="margin: 20px; width: 500px"
        @addButtonClicked="openModal" />
    <CreateUserWindow @show-error="showToast" :isVisible="isModalVisible" @update:isVisible="isModalVisible = $event">
    </CreateUserWindow>
    <Toast v-if="toastVisible" v-model="toastVisible" :message="toastMessage" type="error"
        @close="toastVisible = false" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios'; // Не забудьте импортировать axios
import { NavigationBarForAdmin } from '@/component/trainer';
import { TableUserEdit, CreateUserWindow } from '@/component/trainer';
import { Toast } from '@/component/UI';

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
const headers = ['Пользователь', 'Действие'];

// Динамические данные пользователей
const users = ref<{ id: number; name: string; uuid: string, isBanned: boolean }[]>([]);

// Метод для загрузки данных пользователей с сервера
const fetchUsers = async () => {
    try {
        const response = await axios.get('/api/user/get', { withCredentials: true });
        // Обновляем массив users, добавляя id как индекс + 1 и isBanned
        users.value = response.data.map((user: any, index: number) => ({
            id: index + 1, // Устанавливаем id как индекс + 1
            name: user.login, // Используем поле login для отображения
            uuid: user.uuid, // Добавляем uuid
            isBanned: user.status_id === 1 ? false : true // Определяем значение isBanned
        }));
    } catch (error) {
        console.error('Ошибка при загрузке пользователей:', error);
    }
};

// Загружаем пользователей при монтировании компонента
onMounted(() => {
    fetchUsers();
});

const openModal = () => {
    isModalVisible.value = true;
};
</script>

<style scoped></style>
