<script setup lang="ts">
import { RegisterForm } from '@/component/auth';
import { BaseLogo } from '@/component/trainer';
import ImageUrl from '@/assets/Logo.png';
import { ref } from 'vue';

const loginData = ref('');
const passwordData = ref('');
const repeatPasswordData = ref('');
</script>

<template>
    <div class="container">
        <div class="form-wrapper">
            <BaseLogo :logoSrc="ImageUrl" customStyleForImg="width: 150px; height: 150px;"
                customStyleForText="color: #012E4A; font-family: 'Alata'; font-size: 64px;">
            </BaseLogo>
            <RegisterForm v-model:login="loginData" v-model:password="passwordData"
                v-model:repeatPassword="repeatPasswordData" class="register-form">
            </RegisterForm>
        </div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.form-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.register-form {
    margin-top: 30px;
}
</style>