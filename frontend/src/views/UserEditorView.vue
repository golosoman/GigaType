<template>
    <NavigationBarForAdmin></NavigationBarForAdmin>
    <h2>Редактор пользователей</h2>
    <TableUserEdit :headers="headers" :data="users" customStyle="margin: 20px; width: 500px" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NavigationBarForAdmin } from '@/component/trainer';
import { TableUserEdit } from '@/component/trainer';

const headers = ['Пользователь', 'Действие'];

const users = ref([
    { id: 1, name: 'Иван Иванов' },
    { id: 2, name: 'Мария Петрова' },
    { id: 3, name: 'Сергей Сидоров' }
]);
</script>

<style scoped></style>