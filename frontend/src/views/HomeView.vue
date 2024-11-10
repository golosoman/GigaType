<script setup lang="ts">
import BaseInput from '@/component/UI/BaseInput.vue';
import BaseButton from '@/component/UI/BaseButton.vue';
import BaseInputWithLabel from '@/component/UI/BaseInputWithLabel.vue';
import AuthForm from '@/component/Auth/AuthForm.vue';
import BaseLogo from '@/component/UI/BaseLogo.vue';
import BaseDropdown from '@/component/UI/BaseDropDown.vue';
import TrainingField from '@/component/Trainer/TrainingField.vue';
import BaseCheckbox from '@/component/UI/BaseCheckbox.vue';
import BaseCheckboxGroup from '@/component/UI/BaseCheckboxGroup.vue';
import { ref } from 'vue';
let a = ref("1"); // Просто для теста базовых input
const login = ref('') // Двусторонняя привязка с полем логин в форме auth
const password = ref('') // Двусторонняя привязка с полем пароль в форме auth
const textToType = ref("фыва олдж фыва олдж фыва олдж фыва олдж фыва олдж фыва олдж"); // Текст для поля тренажера
const options = ['Упражнение 1', 'Упражнение 2', 'Упражнение 3']; // Опции для выпадающего списка
const selectedOption = ref(null); // Двусторонняя привязка с опциями
const checkOptions = ['Зона 1(ФЫВАОЛДЖ)', 'Зона 4(МИТЬ)', 'Зона 7(ЁЙЯЗХЪЭ)', 'Зона 2(ПР)', 'Зона 5(УСШБ)', 'Зона 8(1234567890)', 'Зона 3(КЕНГ)', 'Зона 6(ЦЧЩЮ)', 'Зона 9 (Символы)'];
const selectedOptions = ref<string[]>([]);
const handleSelectedValues = (values: string[]) => {
  selectedOptions.value = values;
};
const handleCompletion = (completedText: string) => {
  console.log('Завершено! Введенный текст:', completedText);
};
</script>

<template>
  <main>
    <div>
      <h1>Примеры компонентов</h1>
      <h2>Наш логотип</h2>
      <BaseLogo></BaseLogo>
    </div>
    <div>
      <h2>Базовая кнопка</h2>
      <BaseButton customStyle="width: 200px; height: 50px; background-color: #012E4A; color: #E8EDE7;"
        v-on:click="() => console.log('Базовая кнопка работает! (первая)')">
        click me</BaseButton>
      <BaseButton customStyle="width: 200px; height: 50px;"
        v-on:click="() => console.log('Базовая кнопка работает! (вторая)')">
        click me</BaseButton>

      <BaseButton v-on:click="() => console.log('Базовая кнопка работает! (третья)')">
        click me</BaseButton>
    </div>
    <div>
      <h2>Базовое поле ввода</h2>
      <BaseInput customStyle="width: 800px; height: 50px;" v-model="a"></BaseInput>
      <p>a: {{ a }}</p>
    </div>
    <div>
      <h2>Базовое поле ввода с биркой</h2>
      <BaseInputWithLabel customStyleForInput="width: 800px; height: 50px;" v-model="a" label="Что?!">
      </BaseInputWithLabel>
      <p>a: {{ a }}</p>
    </div>
    <div>
      <h2>Базовый чекбокс</h2>
      <BaseCheckbox label="GG"></BaseCheckbox>
    </div>
    <div>
      <h2>Группа чекбоксов</h2>
      <BaseCheckboxGroup :options="checkOptions" :columns="3" @update:selectedValues="handleSelectedValues" />
      <div>
        <h3>Выбранные опции:</h3>
        <ul>
          <li v-for="option in selectedOptions" :key="option">{{ option }}</li>
        </ul>
      </div>
    </div>
    <div>
      <h2>Выпадающий список</h2>
      <BaseDropdown v-model="selectedOption" :options="options" placeholder="Выберите упражнение" />
      <p>Выбранное упражнение: {{ selectedOption }}</p>
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
      <!-- Кнопки клавы блочатся -->
      <!-- <TrainingField :textToType="textToType" @completed="handleCompletion"
        customStyle="width: 1378px; height: 140px; border-radius: 20px; font-size: 48px; "></TrainingField> -->
    </div>

  </main>
</template>
