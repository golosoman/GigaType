<script setup lang="ts">
import BaseInput from '@/component/UI/BaseInput.vue';
import BaseButton from '@/component/UI/BaseButton.vue';
import BaseInputWithLabel from '@/component/UI/BaseInputWithLabel.vue';
import AuthForm from '@/component/Auth/AuthForm.vue';
import Logo from '@/component/UI/Logo.vue';
import TrainingField from '@/component/Trainer/TrainingField.vue';
import { ref } from 'vue';
let a = ref("1");
const login = ref('')
const password = ref('')
const textToType = ref("фыва олдж фыва олдж фыва олдж фыва олдж фыва олдж фыва олдж");
const handleCompletion = (completedText: string) => {
  console.log('Завершено! Введенный текст:', completedText);
};
</script>

<template>
  <main>
    <div>
      <h1>Примеры компонентов</h1>
      <h2>Наш логотип</h2>
      <Logo></Logo>
    </div>
    <div>
      <h2>Базовая кнопка</h2>
      <BaseButton customStyle="width: 200px; height: 50px; background-color: #012E4A; color: #E8EDE7;"
        v-on:click="() => console.log(423423)">
        click me</BaseButton>
      <BaseButton customStyle="width: 200px; height: 50px;" v-on:click="() => console.log(423423)">
        click me</BaseButton>

      <BaseButton>
        click me</BaseButton>
    </div>
    <div>
      <h2>Базовое поле ввода</h2>
      <BaseInput customStyle="width: 800px; height: 50px;" v-model="a"></BaseInput>
    </div>
    <div>
      <h2>Базовое поле ввода с биркой</h2>
      <BaseInputWithLabel customStyleForInput="width: 800px; height: 50px;" v-model="a" label="Что?!">
      </BaseInputWithLabel>
    </div>
    <div>
      <h2>Форма авторизации</h2>
      <AuthForm v-model:login="login" v-model:password="password"></AuthForm>
      <div>
        <p>Логин: {{ login }}</p>
        <p>Пароль: {{ password }}</p>
      </div>
    </div>
    <div>
      <h2>Поле для тренировки</h2>
      <!-- <TrainingField :textToType="textToType" @completed="handleCompletion"
        customStyle="width: 1378px; height: 140px; border-radius: 20px; font-size: 48px; "></TrainingField> -->
    </div>
  </main>
</template>
