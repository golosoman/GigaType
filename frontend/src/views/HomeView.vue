<script setup lang="ts">
import BaseInput from '@/component/UI/BaseInput.vue';
import BaseButton from '@/component/UI/BaseButton.vue';
import BaseInputWithLabel from '@/component/UI/BaseInputWithLabel.vue';

import { ref } from 'vue';
let a = ref("1");

</script>

<template>
  <main>
    <div>
      <h1>Примеры компонентов</h1>
    </div>
    <div>
      <h2>Базовая кнопка</h2>
      <BaseButton 
        width="200px" 
        height="50px" 
        v-on:click="()=>console.log(423423)"
      >click me</BaseButton>
    </div>
    <div>
      <h2>Базовое поле ввода</h2>
      <BaseInput width="800px" height="50px" v-model="a"></BaseInput>
    </div>
    <div>
      <h2>Базовое поле ввода с биркой</h2>
      <BaseInputWithLabel inputWidth="800px" inputHeight="50px" v-model="a" label="Что?!" ></BaseInputWithLabel>
    </div>
  </main>
</template>
