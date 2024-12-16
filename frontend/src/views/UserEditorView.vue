<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h1>Редактор пользователей</h1>
    <div v-if="isLoading">
        <SpinLoader v-if="isLoading"></SpinLoader>
    </div>
    <div v-else>
        <TableUserEdit :headers="headers" v-model:data="paginatedUsers" customStyle="margin: 20px; width: 500px"
            @addButtonClicked="openModal" />
        <div class="pagination">
            <BaseButton @click="prevPage" :disabled="currentPage === 1"
                custom-style="width: 80px; height: 30px; border-radius:5px; margin-right: 10px;">Назад
            </BaseButton>
            <span style="margin-top: 5px; color: #012e4a;">Страница {{ currentPage }} из {{ totalPages }}</span>
            <BaseButton @click="nextPage" :disabled="currentPage === totalPages"
                custom-style="width: 80px; height: 30px; border-radius:5px; margin-left: 10px;">Вперед</BaseButton>
        </div>
    </div>
    <CreateUserWindow @show-error="showToast" @new-user-add="handleUserAdd" :isVisible="isModalVisible"
        @update:isVisible="isModalVisible = $event">
    </CreateUserWindow>

    <Toast v-if="toastVisible" v-model="toastVisible" :message="toastMessage" type="error"
        @close="toastVisible = false" />
</template>

<script setup lang="ts">
import { ref, onMounted, handleError, computed } from 'vue';
import axios from 'axios'; // Не забудьте импортировать axios
import { TableUserEdit, CreateUserWindow, NavigationBarForAdmin } from '@/component/Trainer';
import { Toast, SpinLoader } from '@/component/UI';
import BaseButton from '@/component/UI/button/BaseButton.vue';

const currentPage = ref(1);
const itemsPerPage = 10;

const isLoading = ref(true); // Состояние загрузки
const toastVisible = ref(false)
const toastMessage = ref('')

const totalPages = computed(() => Math.ceil(users.value.length / itemsPerPage));

const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    return users.value.slice(start, start + itemsPerPage);
});

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

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
const users = ref<{ id: number; name: string; uuid: string; isBanned: boolean }[]>([]);

const handleUserAdd = (user: { name: string, uuid: string, isBanned: boolean }) => {
    users.value.push({
        id: users.value.length + 1,
        name: user.name,
        uuid: user.uuid,
        isBanned: user.isBanned,
    })
}

// Метод для загрузки данных пользователей с сервера
const fetchUsers = async () => {
    isLoading.value = true; // Начинаем загрузку
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
    } finally {
        isLoading.value = false;
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

<style scoped>
h1 {
    margin-left: 15px;
    color: #012e4a;
    font-family: "Alegreya Sans SC";
}

.pagination {
    display: flex;
    justify-content: left;
    margin-left: 15px;
    /* Центрируем кнопки по горизонтали */
    margin-top: 10px;
    /* Отступ сверху */
    margin-bottom: 20px;
    /* Добавляем отступ снизу для отделения от других элементов */
}
</style>
