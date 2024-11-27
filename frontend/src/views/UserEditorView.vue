<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор пользователей</h2>
    <TableUserEdit :headers="headers" :data="users" customStyle="margin: 20px; width: 500px"
        @addButtonClicked="openModal" />
    <CreateUserWindow :isVisible="isModalVisible" @update:isVisible="isModalVisible = $event"></CreateUserWindow>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NavigationBarForAdmin } from '@/component/trainer';
import { TableUserEdit, CreateUserWindow } from '@/component/trainer';

const isModalVisible = ref(false);

const openModal = () => {
    isModalVisible.value = true;
};

const headers = ['Пользователь', 'Действие'];

const users = ref([
    { id: 1, name: 'Иван Иванов' },
    { id: 2, name: 'Мария Петрова' },
    { id: 3, name: 'Сергей Сидоров' }
]);
</script>

<style scoped></style>