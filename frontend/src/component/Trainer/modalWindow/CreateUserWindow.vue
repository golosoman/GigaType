<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Создание нового пользователя
            </div>
            <BaseInputWithLabel label="Логин" inputPlaceholder="Введите логин:" :modelValue="login"
                @update:modelValue="setLogin"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <BaseInputWithLabel label="Пароль" inputPlaceholder="Введите пароль:" :modelValue="password"
                @update:modelValue="setPassword"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" />
            <BaseButton @click="registerUser"
                customStyle="width: 150px; height: 30px; border-radius: 15px; margin-top: 41px; font-size: 20px; color: #012E4A;">
                Сохранить
            </BaseButton>
            <ButtonWithImage class="close-button" @click="closeModal" :imageSrc="CloseUrl"
                customStyle="background-color: #D9D9D9;" customStyleForImage="width: 30px; height: 30px;">
            </ButtonWithImage>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios'; // Импортируем axios
import { KeyboardWithCheckbox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import CloseUrl from '@/assets/Close.png'

export default defineComponent({
    name: 'CreateUser ',
    components: {
        KeyboardWithCheckbox,
        BaseInputWithLabel,
        BaseButton,
        ButtonWithImage
    },
    props: {
        isVisible: {
            type: Boolean,
            required: true,
        },
    },
    setup(props, { emit }) {
        const login = ref('')
        const password = ref('')

        const setLogin = (value: string) => {
            login.value = value
        }

        const setPassword = (value: string) => {
            password.value = value
        }

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const registerUser = async () => {
            try {
                const response = await axios.post('/api/user/register', {
                    login: login.value,
                    password: password.value,
                });

                // Обработка успешного ответа
                console.log('Пользователь успешно создан:', response.data);
                closeModal(); // Закрываем модальное окно после успешного создания
            } catch (error) {
                console.error('Ошибка при создании пользователя:', error);
                // Здесь можно обработать ошибку, например, показать уведомление пользователю
            }
        };

        return {
            login,
            password,
            CloseUrl,
            closeModal,
            setLogin,
            setPassword,
            registerUser  // Возвращаем метод для использования в шаблоне
        };
    },
});
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type="number"] {
    -moz-appearance: textfield;
}

.title {
    font-size: 20px;
    margin-bottom: 10px;
    color: #012E4A;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 3;
}

.modal-content {
    background: #D9D9D9;
    padding: 20px;
    border-radius: 5px;
    position: relative;
    width: 50%;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    border: none;
    background: none;
    cursor: pointer;
    font-size: 20px;
}
</style>