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
                    customStyle="background-color: #86CE81;"></ButtonWithImage>
            </div>
        </div>
        <div class="table-body">
            <div class="table-row" v-for="(user, rowIndex) in data" :key="rowIndex">
                <div class="cell">
                    <BaseLink :href="`/app/user/${user.id}`" target="_blank"
                        style="background-color: transparent; text-decoration: underline; line-height: 30px;">
                        {{ user.name }}
                    </BaseLink>
                </div>
                <div class="cell">
                    <ButtonWithImage :imageSrc="BlockUrl" text="Блокировать"
                        customStyleForImage="width: 20px; height: 20px;" customStyle="background-color: #FA5454; "
                        @click="removeUser(rowIndex)">
                    </ButtonWithImage>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import { ButtonWithImage, BaseLink } from '@/component/UI';
import PlusUrl from '@/assets/Plus.png';
import BlockUrl from '@/assets/Block.png'

const props = defineProps<{
    headers: string[];
    data: Array<{ id: number; name: string }>; // Обновлены поля для пользователей
    customStyle?: string;
}>();

const removeUser = (index: number) => {
    // Здесь вы можете добавить логику для удаления пользователя из данных
    // Например, вы можете использовать emit для уведомления родительского компонента
    // или изменять локальное состояние, если это необходимо.
    console.log(`Удаление пользователя с индексом: ${index}`);
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
    padding: 7px;
    border: 1px solid #012E4A;
    display: flex;
    justify-content: center;
}

.table-row:hover {
    background-color: #D0E8F2;
}
</style>
