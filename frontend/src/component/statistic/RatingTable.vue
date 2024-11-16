<template>
    <div>
        <BaseTable :headers="headers" :data="userData" :style="customStyle" />
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { BaseTable } from '../UI';

// Определяем пропсы
const props = defineProps<{
    userData: Array<{ Место: number; Пользователь: string; Рейтинг: number }>;
    customStyle?: string;
}>();

const headers = ['Место', 'Пользователь', 'Рейтинг'];
</script>

<style scoped></style>
