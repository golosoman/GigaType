<template>
    <table class="base-table" :style="customStyle">
        <thead>
            <tr class="table-header">
                <th v-for="(header, index) in headers" :key="index">
                    {{ header }}
                </th>
            </tr>
        </thead>
        <tbody>
            <tr class="table-row" v-for="(row, rowIndex) in data" :key="rowIndex">
                <td v-for="(header, colIndex) in headers" :key="colIndex">
                    {{ row[header] }}
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps<{
    headers: string[];
    data: Array<Record<string, any>>;
    customStyle?: string;
}>();
</script>

<style scoped>
.base-table {
    width: 100%;
    border-collapse: collapse;
    /* Убирает двойные границы между ячейками */
    border: 1px solid #012E4A;
    color: #012e4a;
    /* Темный синий цвет для границы таблицы */
}

.table-header {
    background-color: #81BECE;
    /* Светлый голубой цвет для фона заголовков */
}

th,
td {
    padding: 15px;
    /* Увеличение отступов для ячеек */
    border: 1px solid #012E4A;
    /* Темный синий цвет для границ ячеек */
    text-align: center;
    /* Выравнивание текста в ячейках по центру */
    min-width: 100px;
    /* Минимальная ширина ячейки */
}

.table-row:hover {
    background-color: #D0E8F2;
    /* Немного более светлый цвет для эффекта наведения */
}
</style>
