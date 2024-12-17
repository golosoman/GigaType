<template>
    <div>
        <BaseTable :headers="headers" :data="tableData" :customStyle="customStyle" />
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { BaseTable } from '@/component/UI';

// Определяем пропсы
const props = defineProps<{
    tableData: Array<{
        Упражнение: number;
        Статус: string;
        Скорость: string;
        Ошибки: string;
        Время: string;
    }>;
    customStyle?: string;
}>();

const headers = ['Упражнение', 'Статус', 'Скорость', 'Ошибки', 'Время', 'Дата'];
</script>

<style scoped>
/* Добавьте стили для вашего компонента, если необходимо */
</style>
