<script lang="ts">
import { BaseLogo } from "../logo";
import { BaseInputWithLabel, BaseButton, BaseLink } from "@/component/UI";
import { defineComponent, ref } from 'vue';
import { useUser } from '@/store/index';
import { useRouter } from 'vue-router'; // Импортируем useRouter

export default defineComponent({
    name: 'AuthForm',
    components: {
        BaseButton,
        BaseLogo,
        BaseInputWithLabel,
        BaseLink
    },
    props: {
        customStyle: {
            type: String,
            required: false,
            default: '',
        },
    },
    setup(props, { emit }) {
        const userStore = useUser(); // Используем хранилище пользователей
        const router = useRouter(); // Получаем экземпляр роутер
        const loginData = ref({ login: '', password: '' }); // Создаем объект для хранения логина и пароля

        const handleLogin = async () => {
            try {
                await userStore.loginUser(loginData.value); // Вызываем метод авторизации
                console.log("Успешный вход"); // Успешный вход

                // Перенаправление в зависимости от роли
                if (userStore.role === 'ADMIN') {
                    router.push('/app/cabinet/admin'); // Перенаправляем администратора
                } else {
                    router.push('/app/cabinet/trainee'); // Перенаправляем обычного пользователя
                }
            } catch (error) {
                console.error('Ошибка входа:', error); // Обработка ошибки
            }
        };

        const changePassword = (password: string) => {
            loginData.value.password = password; // Обновляем пароль в объекте
            emit('update:password', password);
        }

        const changeLogin = (login: string) => {
            loginData.value.login = login; // Обновляем логин в объекте
            emit('update:login', login);
        }

        // Добавьте loginData в return
        return {
            loginData,
            changePassword,
            changeLogin,
            handleLogin
        };
    }
})
</script>

<template>
    <div>
        <div class="formContent" :style="customStyle">
            <div>
                <form @submit.prevent="handleLogin"> <!-- Измените на вызов handleLogin при отправке -->
                    <div class="formGroup">
                        <BaseInputWithLabel label="Логин" inputPlaceholder="Введите логин:"
                            :modelValue="loginData.login" @update:modelValue="changeLogin" style="margin-top: 46px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <BaseInputWithLabel label="Пароль" inputPlaceholder="Введите пароль:"
                            :modelValue="loginData.password" inputType="password" @update:modelValue="changePassword"
                            style="margin-top: 38px;" customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <BaseButton type="submit"
                            customStyle="width: 171px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
                            Войти
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
    height: 435px;
    background-color: #D9E1E5;
}

.formGroup {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
