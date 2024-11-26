<template>
    <div class="base-table" :style="customStyle">
        <div class="table-header">
            <div class="header-cell" v-for="(header, index) in headers" :key="index">
                {{ header }}
            </div>
        </div>
        <div>
            <div class="header-cell centered-cell" colspan="2">
                <ButtonWithImage :imageSrc="PlusUrl"
                    customStyleForImage="width: 20px; height: 20px; margin-top: 2px; margin-bottom: 2px;"
                    customStyle="background-color: #86CE81;"></ButtonWithImage>
            </div>
        </div>
        <div class="table-body">
            <div class="table-row" v-for="(row, rowIndex) in data" :key="rowIndex">
                <div class="cell" v-for="(header, colIndex) in headers" :key="colIndex">
                    <template v-if="'Название' === header">
                        <a :href="`/app/choose_exercise/level/${row.level}/exercise/${row.number}`" target="_blank">
                            Упражнение {{ row["level"] }}.{{ row['number'] }}
                        </a>
                    </template>
                    <template v-else>
                        {{ row['value'] }} <!-- Предполагаем, что у вас есть поле 'value' -->
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { ButtonWithImage } from '@/component/UI';
import PlusUrl from '@/assets/Plus.png';

const props = defineProps<{
    headers: string[];
    data: Array<{ name: string; value: number; level: number; number: number }>; // Добавлены поля 'level' и 'number'
    customStyle?: string;
}>();
</script>

<style scoped>
.centered-cell {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.base-table {
    display: flex;
    flex-direction: column;
    width: 100%;
    border: 1px solid #012E4A;
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