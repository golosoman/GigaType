<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Создание нового пользователя
            </div>
            <BaseInputWithLabel label="Логин" inputPlaceholder="Введите логин:" :modelValue="login"
                @update:modelValue="onLoginInput"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <div v-if="loginError" style="color: red;">{{ loginError }}</div>

            <BaseInputWithLabel label="Пароль" inputPlaceholder="Введите пароль:" :modelValue="password"
                inputType="password" @update:modelValue="onPasswordInput"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" />
            <div v-if="passwordError" style="color: red;">{{ passwordError }}</div>

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
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import CloseUrl from '@/assets/Close.png';
import { validateLogin, validatePassword } from '@/utils';

export default defineComponent({
    name: 'CreateUser ',
    components: {
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
        const login = ref('');
        const password = ref('');
        const loginError = ref('');
        const passwordError = ref('');

        const resetValues = () => {
            login.value = '';
            password.value = '';
            loginError.value = '';
            passwordError.value = '';
        }

        const closeModal = () => {
            resetValues()
            emit('update:isVisible', false);
        };

        const onLoginInput = (value: string) => {
            login.value = value; // Обновляем значение логина
            validateLogin(value, loginError); // Обновляем ошибку
        };

        const onPasswordInput = (value: string) => {
            password.value = value; // Обновляем значение пароля
            validatePassword(value, passwordError); // Обновляем ошибку
        };

        const registerUser = async () => {
            // Валидация перед отправкой
            if (loginError.value || passwordError.value) {
                emit('show-error', loginError.value || passwordError.value);
                return;
            }

            try {
                const response = await axios.post('/api/user/register', {
                    login: login.value,
                    password: password.value,
                });

                emit("new-user-add", {
                    name: login.value, // Используем логин
                    uuid: response.data.uuid, // UUID нового пользователя
                    isBanned: false // Новый пользователь не заблокирован
                });

                // Обработка успешного ответа
                console.log('Пользователь успешно создан:', response.data);
                closeModal(); // Закрываем модальное окно после успешного создания
            } catch (error) {
                // Приведение типа ошибки
                if (axios.isAxiosError(error) && error.response) {
                    if (error.response.status === 418) {
                        emit('show-error', 'Пользователь с таким логином уже существует.');
                    } else {
                        const errorMessage = 'Ошибка регистрации. Пожалуйста, попробуйте еще раз.';
                        emit('show-error', errorMessage);
                    }
                } else {
                    emit('show-error', 'Неизвестная ошибка. Пожалуйста, попробуйте еще раз.');
                }
            }
        };


        return {
            login,
            password,
            loginError,
            passwordError,
            CloseUrl,
            closeModal,
            onLoginInput,
            onPasswordInput,
            registerUser
        };
    },
});
</script>

<style scoped>
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

Найти еще