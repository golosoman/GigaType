<script setup lang="ts">
import BaseInput from '@/component/UI';
import BaseButton from '@/component/UI';
import BaseInputWithLabel from '@/component/UI';
import AuthForm from '@/component/Auth/AuthForm.vue';
import BaseLogo from '@/component/UI';
import BaseDropdown from '@/component/UI';
import TrainingField from '@/component/Trainer/TrainingField.vue';
import BaseCheckbox from '@/component/UI';
import BaseCheckboxGroup from '@/component/UI';
import Toast from '@/component/UI';
import TypingTrainer from '@/component/Trainer/TypingTrainer.vue';
import BaseLink from '@/component/UI';
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
const toastVisible = ref(false);
const toastMessage = ref('');
const toastType = ref('info');

const showToast = (message: string, type: string) => {
  toastMessage.value = message;
  toastType.value = type;
  toastVisible.value = true;
};
const handleCompletion = (completedText: string) => {
  console.log('Завершено! Введенный текст:', completedText);
};

//------------------------------------------------------------Тренажер
// Определяем интерфейс для данных о завершении
interface CompletionData {
  level: string;
  exercise: string;
  speed: number;
  errorsCount: number;
  elapsedTime: number;
  score: number;
}

const successData = ref<CompletionData | null>(null);
const errorData = ref<CompletionData | null>(null);

const handleSuccessCompletion = (data: any[]) => {
  successData.value = {
    level: data[0],
    exercise: data[1],
    speed: data[2],
    errorsCount: data[3],
    elapsedTime: data[4],
    score: data[5],
  };
  errorData.value = null; // Сбросить данные об ошибках, если они были
};

const handleErrorCompletion = (data: any[]) => {
  errorData.value = {
    level: data[0],
    exercise: data[1],
    speed: data[2],
    errorsCount: data[3],
    elapsedTime: data[4],
    score: data[5],
  };
  successData.value = null; // Сбросить данные о успешном завершении, если они были
};

</script>

<template>
  <main>
    <div>
      <h1>Примеры компонентов</h1>
      <h2>Наш логотип</h2>
      <BaseLogo customStyleForImg="width: 90px; height: auto;"></BaseLogo>
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
      <BaseLink href="https://example.com" customStyle="width: 200px; height: 50px;">
        Перейти на Example.com
      </BaseLink>
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
      <BaseCheckboxGroup :options="checkOptions" :columns="3" customStyle="width: 570px"
        @update:selectedValues="handleSelectedValues" />
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
      <h2>Уведомления для пользователя</h2>
      <button @click="showToast('Это сообщение об ошибке!', 'error')">Показать ошибку</button>
      <button @click="showToast('Это сообщение об успешном действии!', 'success')">Показать успех</button>
      <button @click="showToast('Это информационное сообщение.', 'info')">Показать информацию</button>
      <button @click="showToast('Это предупреждение!', 'warning')">Показать предупреждение</button>

      <Toast v-if="toastVisible" v-model="toastVisible" :message="toastMessage" :type="toastType"
        @close="toastVisible = false" />
    </div>
    <div>
      <h2>Поле для тренировки</h2>
      <!-- Кнопки клавы блочатся -->
      <!-- <TrainingField :textToType="textToType" @completed="handleCompletion"
        customStyle="width: 1378px; height: 140px; border-radius: 20px; font-size: 48px; "></TrainingField> -->
    </div>
    <div>
      <h2>Клавиатурный тренажер</h2>
      <TypingTrainer level="Легкий" exercise="Печать текста" :maxErrors="5" textToType="Пример текста для тренировки."
        customStyleForTrainingField="width: 1378px; height: 140px; border-radius: 20px; font-size: 48px; "
        @success-completion="handleSuccessCompletion" @error-completion="handleErrorCompletion" />
      <div v-if="successData">
        <h3>Успешное завершение:</h3>
        <p>Уровень: {{ successData.level }}</p>
        <p>Упражнение: {{ successData.exercise }}</p>
        <p>Скорость: {{ successData.speed }} симв/мин</p>
        <p>Ошибки: {{ successData.errorsCount }}</p>
        <p>Время: {{ successData.elapsedTime }} сек</p>
        <p>Счет: {{ successData.score }}</p>
      </div>
      <div v-if="errorData">
        <h3>Завершение с ошибками:</h3>
        <p>Уровень: {{ errorData.level }}</p>
        <p>Упражнение: {{ errorData.exercise }}</p>
        <p>Скорость: {{ errorData.speed }} симв/мин</p>
        <p>Ошибки: {{ errorData.errorsCount }}</p>
        <p>Время: {{ errorData.elapsedTime }} сек</p>
        <p>Счет: {{ errorData.score }}</p>
      </div>
    </div>
  </main>
</template>
