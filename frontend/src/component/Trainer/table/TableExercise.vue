<template>
    <div class="base-table" :style="customStyle">
        <div class="table-header">
            <div class="header-cell" v-for="(header, index) in headers" :key="index">
                {{ header }}
            </div>
        </div>
        <div class="table-body">
            <div class="table-row" v-for="(row, rowIndex) in data" :key="rowIndex">
                <div class="cell" v-for="(header, colIndex) in headers" :key="colIndex">
                    <template v-if="'Название' === header">
                        <BaseLink href="#" @click.prevent="handleExerciseClick(row.levelId, row.taskId)"
                            style="background-color: transparent; text-decoration: underline; line-height: 20px;">
                            Упражнение {{ row.level }}.{{ row.exercise }}
                        </BaseLink>
                    </template>
                    <template v-else>
                        {{ row.exercise }}
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { BaseLink } from '@/component/UI';
import { defineProps } from 'vue';
import { useRouter } from 'vue-router'; // Импортируем useRouter
import { useUser } from '@/store'; // Импортируем store

const props = defineProps<{
    headers: string[];
    data: Array<Record<string, any>>;
    customStyle?: string;
}>();

const router = useRouter(); // Получаем доступ к маршрутизатору
const userStore = useUser(); // Получаем доступ к store

const handleExerciseClick = (levelId: string, taskId: string) => {
    userStore.selectExercise(levelId, taskId); // Сохраняем выбор в store
    router.push(`/app/trainer/${levelId}/${taskId}`); // Перенаправляем
};
</script>

<style scoped>
.base-table {
    display: flex;
    flex-direction: column;
    width: 100%;
    border: 1px solid #012E4A;
    color: #012e4a;
}

.table-header {
    display: flex;
    background-color: #81BECE;
}

.header-cell {
    flex: 1;
    padding: 10px;
    font-weight: bold;
    text-align: left;
    border: 1px solid #012E4A;
}

.table-body {
    display: flex;
    flex-direction: column;
}

.table-row {
    display: flex;
}

.cell {
    flex: 1;
    padding: 10px;
    border: 1px solid #012E4A;
}

.table-row:hover {
    background-color: #D0E8F2;
}
</style>
