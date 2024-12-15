<script lang="ts">
import { BaseLogo } from "../logo";
import { BaseInputWithLabel, BaseButton, BaseLink } from "@/component/UI";
import { defineComponent, ref } from 'vue';
import { useUser } from '@/store'; // Импортируем store
import { useRouter } from 'vue-router'; // Импортируем useRouter
import type axios from "axios";
import { validateLogin, validatePassword, validateRepeatPassword } from "@/utils";

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

        const handleLoginInput = (value: string) => {
            validateLogin(value, loginError);
            emit('update:login', value);
        };

        const handlePasswordInput = (value: string) => {
            validatePassword(value, passwordError);
            emit('update:password', value);
        };

        const handleRepeatPasswordInput = (value: string) => {
            validateRepeatPassword(value, props.password, repeatPasswordError);
            emit('update:repeatPassword', value);
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
            handleLoginInput,
            handlePasswordInput,
            handleRepeatPasswordInput
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
                            @update:modelValue="handleLoginInput" style="margin-top: 46px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <div v-if="loginError" style="color: red;">{{ loginError }}</div>

                        <BaseInputWithLabel label="Пароль" inputPlaceholder="Введите пароль:" :modelValue="password"
                            inputType="password" @update:modelValue="handlePasswordInput" style="margin-top: 38px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <div v-if="passwordError" style="color: red;">{{ passwordError }}</div>

                        <BaseInputWithLabel label="Подтверждение пароля" inputPlaceholder="Подтвердите пароль:"
                            inputType="password" :modelValue="repeatPassword"
                            @update:modelValue="handleRepeatPasswordInput" style="margin-top: 38px;"
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
