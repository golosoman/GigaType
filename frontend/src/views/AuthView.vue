<script setup lang="ts">
import { AuthForm } from '@/component/auth';
import { BaseLogo } from '@/component/trainer';
import ImageUrl from '@/assets/Logo.png';
import { ref } from 'vue';

const loginData = ref('');
const passwordData = ref('');
</script>

<template>
    <div class="container">
        <div class="form-wrapper">
            <BaseLogo :logoSrc="ImageUrl" customStyleForImg="width: 150px; height: 150px;"
                customStyleForText="color: #012E4A; font-family: 'Alata'; font-size: 64px;">
            </BaseLogo>
            <AuthForm v-model:login="loginData" v-model:password="passwordData" class="auth-form" />
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

.auth-form {
    margin-top: 30px;
}
</style>
