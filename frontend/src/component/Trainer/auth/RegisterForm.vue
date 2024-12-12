<script lang="ts">
import { BaseLogo } from "../logo";
import { BaseInputWithLabel, BaseButton, BaseLink } from "@/component/UI";
import { defineComponent, ref } from 'vue';
import { useUser } from '@/store'; // Импортируем store
import { useRouter } from 'vue-router'; // Импортируем useRouter
import type axios from "axios";

export default defineComponent({
    name: 'RegisterForm',
    components: {
        BaseLink,
        BaseLogo,
        BaseInputWithLabel,
        BaseButton
    },
    props: {
        login: {
            type: String,
            required: true,
        },
        password: {
            type: String,
            required: true,
        },
        repeatPassword: {
            type: String,
            required: true,
        },
        customStyle: {
            type: String,
            required: false,
            default: '',
        },
    },
    setup(props, { emit }) {
        const userStore = useUser(); // Используем хранилище пользователей
        const router = useRouter(); // Получаем экземпляр роутер
        const loginError = ref('');
        const passwordError = ref('');
        const repeatPasswordError = ref('');

        const validateLogin = (login: string) => {
            if (login.length < 4) {
                loginError.value = 'Логин должен содержать минимум 4 символа.';
            } else if (login.length > 10) {
                loginError.value = 'Логин не может превышать 10 символов.';
            } else {
                loginError.value = '';
            }
            emit('update:login', login);
        };

        const validatePassword = (password: string) => {
            if (password.length < 4) {
                passwordError.value = 'Пароль должен содержать минимум 4 символа.';
            } else if (password.length > 10) {
                passwordError.value = 'Пароль не может превышать 10 символов.';
            } else {
                passwordError.value = '';
            }
            emit('update:password', password);
        };

        const validateRepeatPassword = (repeatPassword: string) => {
            if (repeatPassword !== props.password) {
                repeatPasswordError.value = 'Пароли не совпадают.';
            } else {
                repeatPasswordError.value = '';
            }
            emit('update:repeatPassword', repeatPassword);
        };

        const handleSubmit = async () => {
            if (loginError.value || passwordError.value || repeatPasswordError.value) {
                emit('show-error', loginError.value || passwordError.value || repeatPasswordError.value);
                return;
            }

            try {
                await userStore.register({ login: props.login, password: props.password });
                emit('register-success', { login: props.login, password: props.password });
                router.push('/app/cabinet/trainee'); // Перенаправляем обычного пользователя
            } catch (error: any) {
                // Обработка ошибок от сервера
                if (error.response && error.response.status === 418) {
                    emit('show-error', 'Пользователь с таким логином уже существует.');
                } else {
                    const errorMessage = 'Ошибка регистрации. Пожалуйста, попробуйте еще раз.';
                    emit('show-error', errorMessage);
                }
            }
        };

        return {
            validateLogin,
            validatePassword,
            validateRepeatPassword,
            handleSubmit,
            loginError,
            passwordError,
            repeatPasswordError,
        };
    }
});
</script>

<template>
    <div>
        <div class="formContent" :style="customStyle">
            <div>
                <form @submit.prevent="handleSubmit">
                    <div class="formGroup">
                        <BaseInputWithLabel label="Логин" inputPlaceholder="Введите логин:" :modelValue="login"
                            @update:modelValue="validateLogin" style="margin-top: 46px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <div v-if="loginError" style="color: red;">{{ loginError }}</div>

                        <BaseInputWithLabel label="Пароль" inputPlaceholder="Введите пароль:" :modelValue="password"
                            inputType="password" @update:modelValue="validatePassword" style="margin-top: 38px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <div v-if="passwordError" style="color: red;">{{ passwordError }}</div>

                        <BaseInputWithLabel label="Подтверждение пароля" inputPlaceholder="Подтвердите пароль:"
                            inputType="password" :modelValue="repeatPassword"
                            @update:modelValue="validateRepeatPassword" style="margin-top: 38px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <div v-if="repeatPasswordError" style="color: red;">{{ repeatPasswordError }}</div>

                        <BaseButton
                            customStyle="width: 338px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
                            Зарегистрироваться
                        </BaseButton>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.headerButton {
    display: flex;
}

.formContent {
    width: 502px;
    height: 571px;
    background-color: #D9E1E5;
}

.formGroup {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
