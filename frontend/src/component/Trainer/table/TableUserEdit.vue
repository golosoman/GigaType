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
            <div class="table-row" v-for="(user, rowIndex) in data" :key="user.id">
                <div class="cell">
                    <BaseLink :href="`/app/user/${user.id}`" target="_blank"
                        style="background-color: transparent; text-decoration: underline; line-height: 30px;">
                        {{ user.name }}
                    </BaseLink>
                </div>
                <div class="cell">
                    <ButtonWithImage :imageSrc="BlockUrl" :text="user.isBanned ? 'Разблокировать' : 'Заблокировать'"
                        customStyleForImage="width: 20px; height: 20px;"
                        :customStyle="user.isBanned ? 'background-color: #6492FF;' : 'background-color: #FF8080;'"
                        @click="removeUser(user.uuid, user.isBanned)">
                    </ButtonWithImage>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { ButtonWithImage, BaseLink } from '@/component/UI';
import PlusUrl from '@/assets/Plus.png';
import BlockUrl from '@/assets/Block.png';
import axios from 'axios'; // Импортируем axios

const props = defineProps<{
    headers: string[];
    data: Array<{ id: number; name: string; uuid: string; isBanned: boolean }>; // Обновлены поля для пользователей
    customStyle?: string;
}>();

const emit = defineEmits<{
    (e: 'addButtonClicked'): void; // Определяем событие addButtonClicked
}>();

const handleAddButtonClick = () => {
    emit('addButtonClicked'); // Генерируем событие при нажатии на кнопку
    console.log('Кнопка "Добавить" нажата'); // Лог для проверки
};

const removeUser = async (uuid: string, isBanned: boolean) => {
    const url = isBanned
        ? '/api/user/unblock'
        : '/api/user/block';

    const body = { "uuid": uuid };
    console.log(body)
    try {
        const response = await axios.post(url, body, {
            headers: {
                'Content-Type': 'application/json',
            },
            withCredentials: true,
        });
        console.log('Успешно изменено состояние пользователя:', response.data);

        // Здесь вы можете обновить состояние пользователя в вашем компоненте, если это необходимо
        // Например, если вы используете реактивный массив users
    } catch (error) {
        console.error('Ошибка при изменении состояния пользователя:', error);
    }
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

Найти еще