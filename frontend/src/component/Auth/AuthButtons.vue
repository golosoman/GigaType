<template>
    <div class="headerButton">
        <BaseButton :customStyle="loginButtonStyle" @click="changeForm('login')">
            Вход
        </BaseButton>
        <BaseButton :customStyle="registerButtonStyle" @click="changeForm('register')">
            Регистрация
        </BaseButton>
    </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { BaseButton } from '../UI';
// import BaseLink from '../UI/link/BaseLink.vue';

export default defineComponent({
    name: 'AuthButtons',
    components: {
        BaseButton,
    },
    props: {
        currentForm: {
            type: String,
            required: true,
        },
        loginLinkStyles: {
            type: String,
            required: true,
        },
        registerLinkStyles: {
            type: String,
            required: true,
        },
    },
    setup(props, { emit }) {
        const changeForm = (form: string) => {
            emit('update:currentForm', form);
        };

        // Вычисляемые свойства для стилей кнопок
        const loginButtonStyle = computed(() => {
            return props.currentForm === 'login'
                ? props.loginLinkStyles + "background-color: #012E4A; color: #E8EDE7;"
                : props.loginLinkStyles
        });

        const registerButtonStyle = computed(() => {
            return props.currentForm === 'register'
                ? props.registerLinkStyles + "background-color: #012E4A; color: #E8EDE7;"
                : props.registerLinkStyles
        });

        return { changeForm, loginButtonStyle, registerButtonStyle };
    },
});
</script>

<style scoped>
.headerButton {
    display: flex;
    color: #012E4A;
}
</style>