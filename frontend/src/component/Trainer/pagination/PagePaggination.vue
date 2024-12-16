<template>
    <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Назад</button>
        <span>Страница {{ currentPage }} из {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Вперед</button>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps<{
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
}>();

const nextPage = () => {
    if (props.currentPage < props.totalPages) {
        props.onPageChange(props.currentPage + 1);
    }
};

const prevPage = () => {
    if (props.currentPage > 1) {
        props.onPageChange(props.currentPage - 1);
    }
};
</script>

<style scoped>
.pagination {
    display: flex;
    justify-content: left;
    margin-left: 15px;
    margin-top: 10px;
    margin-bottom: 20px;
}

.pagination button {
    margin: 0 5px;
    padding: 5px 10px;
    background-color: #81BECE;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.pagination button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}
</style>
