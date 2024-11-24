<template>
    <div class="container">
        <div class="form-wrapper">
            <BaseLogo :logoSrc="ImageUrl" customStyleForImg="width: 150px; height: 150px;"
                customStyleForText="color: #012E4A; font-family: 'Alata'; font-size: 64px;">
            </BaseLogo>
            <div style="margin-top: 30px">
                <AuthButtons v-model:currentForm="currentForm"
                    loginLinkStyles="width: 251px; height: 61px; text-align: left; font-size: 32px; padding-left: 10px; border-radius: 15px 0px 0px 0px;"
                    registerLinkStyles="width: 251px; height: 61px; text-align: left; font-size: 32px; padding-left: 10px; border-radius: 0px 15px 0px 0px;"
                    @update:currentForm="changeForm" />
                <div v-if="currentForm === 'login'">
                    <AuthForm v-model:login="login" v-model:password="password"
                        customStyle="border-radius: 0px 0px 15px 15px;" />
                </div>
                <div v-else>
                    <RegisterForm v-model:login="login" v-model:password="password"
                        v-model:repeatPassword="repeatPassword" customStyle="border-radius: 0px 0px 15px 15px;" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { BaseLogo, AuthButtons, AuthForm, RegisterForm } from '@/component/trainer';
import ImageUrl from '@/assets/Logo.png';
import { ref } from 'vue'

const currentForm = ref('login')
const login = ref('')
const password = ref('')
const repeatPassword = ref('')

const changeForm = (form: string) => {
    currentForm.value = form;
    login.value = ''
    password.value = ''
    repeatPassword.value = ''
}     
</script>

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
</style>