<template>
    <div class="base-table" :style="customStyle">
        <div class="table-header">
            <div class="header-cell" v-for="(header, index) in headers" :key="index">
                {{ header }}
            </div>
        </div>
        <div>
            <div class="header-cell centered-cell" colspan="2">
                <ButtonWithImage :imageSrc="PlusUrl" text="Добавить"
                    customStyleForImage="width: 20px; height: 20px; margin-top: 2px; margin-bottom: 2px;"
                    customStyle="background-color: #86CE81;" @click="handleAddButtonClick"></ButtonWithImage>
            </div>
        </div>
        <div class="table-body">
            <div class="table-row" v-for="(row, rowIndex) in levels" :key="rowIndex">
                <div class="cell" v-for="(header, colIndex) in headers" :key="colIndex">
                    <template v-if="'Название' === header">
                        <BaseLink href="#" target="_blank"
                            style="background-color: transparent; text-decoration: underline; line-height: 20px;"
                            @click.prevent="handleLevelClick(row.uid)">
                            Уровень {{ row.level }}
                        </BaseLink>
                    </template>
                    <template v-else>
                        {{ row.level }}
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, watch, ref } from 'vue';
import { ButtonWithImage, BaseLink } from '@/component/UI';
import PlusUrl from '@/assets/Plus.png';

const props = defineProps<{
    headers: string[];
    data: Array<{ level: number; name: string; uid: string }>; // Теперь добавлено поле uid
    customStyle?: string;
}>();

const levels = ref(props.data)

watch(() => props.data, (levelData) => {
    levels.value = levelData;
    console.log(`Уровни изменились! ${levelData}`);
});


const emit = defineEmits<{
    (e: 'createButtonClick'): void; // Определяем событие addButtonClicked
    (e: 'levelClick', uid: string): void; // Определяем событие для клика по уровню
}>();

const handleAddButtonClick = () => {
    emit('createButtonClick'); // Генерируем событие при нажатии на кнопку
    console.log('Кнопка "Добавить" нажата'); // Лог для проверки
};

const handleLevelClick = (uid: string) => {
    emit('levelClick', uid); // Генерируем событие с uid при клике на уровень
};
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
    text-align: center;
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
    text-align: center;
}

.table-row:hover {
    background-color: #D0E8F2;
}
</style>
