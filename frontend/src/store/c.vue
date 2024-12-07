<template>
    <div>
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
            <input v-model="loginData.login" type="text" placeholder="Login" />
            <input v-model="loginData.password" type="password" placeholder="Password"  />
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useUser } from '@/store/index'; // Исправлено имя

const userStore = useUser();
const loginData = ref({ login: '', password: '' });

const handleLogin = async () => {
    try {
        await userStore.loginUser(loginData.value);
        console.log("Зарегался");
    } catch (error) {
        console.error('Login failed:', error);
    }
};
</script>