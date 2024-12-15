<script setup lang="ts">

import {
  TrainingField,
  Keyboard,
  KeyboardButton,
  TypingTrainer,
  BaseLogo,
  NavigationBarForTrainee,
  AuthButtons,
  AuthForm,
  RegisterForm,
  NavigationBarForAdmin,
  KeyboardWithCheckbox,
  CreateLevelWindow,
  EditLevelWindow,
  CreateExerciseWindow,
  EditExerciseWindow
} from '@/component/Trainer';
import ImageUrl from '@/assets/Logo.png'
import UserUrl from '@/assets/User.png'
import CloseUrl from '@/assets/Close.png'
import { ref } from 'vue';
import {
  BaseButton,
  BaseInput,
  BaseInputWithLabel,
  BaseDropdown,
  BaseCheckbox,
  BaseCheckboxGroup,
  Toast,
  BaseLink,
  ImageLink,
  BaseImage,
  BaseTable,
  ButtonWithImage,
  CheckBoxGroupWithBlock
} from '@/component/UI'

const imgUrl = ref(ImageUrl);
let a = ref("1"); // Просто для теста базовых input
const login = ref('') // Двусторонняя привязка с полем логин в форме auth
const password = ref('') // Двусторонняя привязка с полем пароль в форме auth
const repeatPassword = ref('') // Двусторонняя привязка с полем пароль в форме auth
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

const currentCharacter = ref('');

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

interface Key {
  values: string[];
  backgroundColor?: string;
}

const keys = ref<Key[]>([
  { values: [' '] }, // Кнопка пробела
  { values: ['1', '!'] },
  { values: ['2', '@'] },
  { values: ['3', '#'] },
  { values: ['К'] },
  // Добавьте остальные кнопки
]);

const tableHeaders = ['Имя', 'Возраст', 'Город'];
const tableData = [
  { Имя: 'Иван', Возраст: 25, Город: 'Москва' },
  { Имя: 'Анна', Возраст: 30, Город: 'Санкт-Петербург' },
  { Имя: 'Петр', Возраст: 22, Город: 'Екатеринбург' },
];

const chartData = ref([
  { date: '2023-01-01', new: 10, old: 5 },
  { date: '2023-01-02', new: 15, old: 10 },
  { date: '2023-01-03', new: 20, old: 15 },
])

const isModalVisible = ref(false);

const showModal = () => {
  isModalVisible.value = true;
};

const closeModal = () => {
  isModalVisible.value = false;
};



const isModalVisible2 = ref(false);

// Пример массива зон клавиатуры
const keyboardZones = [
  'Зона 1 (ФЫВАОЛДЖ)',
  'Зона 3 (КЕНГ)',
  'Зона 4 (МИТЬ)',
  'Зона 7 (ЁЙЯЗХЪЭ.,)',
];

const checkboxOptions = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5'];
const selectedCheckboxess = ref(['Option 1', 'Option 3']); // Пример выбранных значений

const updateSelectedCheckboxes = (newValues: string[]) => {
  selectedCheckboxess.value = newValues;
};

// Пример минимального и максимального количества символов
const minCount = ref(30);
const maxCount = ref(80);
const pressTime = ref(1.5)

const openModal = () => {
  isModalVisible2.value = true;
};

const isModalVisible3 = ref(false);

const openModal3 = () => {
  isModalVisible3.value = true;
};

const textExercise = ref("Это текст упражнения, который потом пользователь будет вводить...")

const isModalVisible4 = ref(false);

const openModal4 = () => {
  isModalVisible4.value = true;
};
</script>

<template>
  <main>
    <h1>Примеры компонентов</h1>
    <div>
      <h2>Навигационная панель пользователя</h2>
      <NavigationBarForTrainee></NavigationBarForTrainee>
    </div>
    <div>
      <h2>Навигационная панель администратора</h2>
      <NavigationBarForAdmin></NavigationBarForAdmin>
    </div>
    <div>
      <h2>Наш логотип</h2>
      <BaseLogo :logoSrc="imgUrl" customStyleForImg="width: 90px; height: auto;">
      </BaseLogo>
    </div>
    <div>
      <h2>Картинка</h2>
      <BaseImage :src="UserUrl" alt="asdsad"></BaseImage>
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
      <h2>Кнопка-ссылка</h2>
      <BaseLink href="https://example.com" customStyle="width: 200px; height: 50px;">
        Перейти на Example.com
      </BaseLink>
    </div>
    <div>
      <h2>Ссылка-картинка</h2>
      <ImageLink url="https://example.com" customStyle="width: 50px; height: 50px;" :imageSrc="imgUrl"></ImageLink>
    </div>
    <div>
      <h2>Базовое поле ввода</h2>
      <BaseInput customStyle="width: 800px; height: 50px;" v-model="a"></BaseInput>
      <p>a: {{ a }}</p>
    </div>
    <div>
      <h2>Кнопка с картинкой</h2>
      <ButtonWithImage :image-src="CloseUrl"></ButtonWithImage>
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
      <h2>Группа чекбоксов с блокировкой</h2>
      <CheckBoxGroupWithBlock :options="checkboxOptions" :valuesSelected="selectedCheckboxess"
        @update:selectedValues="updateSelectedCheckboxes" :columns="3" customStyle="margin: 20px;"
        customStyleForBaseCheckbox="margin-bottom: 10px;"></CheckBoxGroupWithBlock>
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
      <h2>Форма регистрации</h2>
      <RegisterForm v-model:login="login" v-model:password="password" v-model:repeatPassword="repeatPassword">
      </RegisterForm>
      <div>
        <p>Логин: {{ login }}</p>
        <p>Пароль: {{ password }}</p>
        <p>Повтор пароля: {{ repeatPassword }}</p>
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
      <h2>Клавиатура с чек-боксами</h2>
      <KeyboardWithCheckbox @update:selectedValues="handleSelectedValues"></KeyboardWithCheckbox>
      <div>
        <h3>Выбранные опции:</h3>
        <ul>
          <li v-for="option in selectedOptions" :key="option">{{ option }}</li>
        </ul>
      </div>
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
    <div>
      <h2>Кнопки</h2>
      <div class="keyboard-container">
        <KeyboardButton v-for="(key, index) in keys" :key="index" :values="key.values"
          :backgroundColor="key.backgroundColor"
          custom-style="background-color: #E8EDE7; width: 90px; height: 90px; font-size: 30px; border-radius: 10px;" />
      </div>
    </div>
    <div>
      <h2>Модальное окно создания уровней сложности</h2>
      <div>
        <button @click="showModal">Создать уровень сложности</button>
        <CreateLevelWindow :isVisible="isModalVisible" @update:isVisible="isModalVisible = $event">
          <h2>Это модальное окно</h2>
          <p>Содержимое модального окна.</p>
          <button @click="closeModal">Закрыть</button>
        </CreateLevelWindow>
      </div>
    </div>
    <div>
      <h2>Модальное окно изменения уровней сложности</h2>
      <button @click="openModal">Изменить уровень сложности</button>
      <EditLevelWindow :isVisible="isModalVisible2" :keyboardZones="keyboardZones" :minCount="minCount"
        :timePressKey="pressTime" :maxCount="maxCount" @update:isVisible="isModalVisible2 = $event" />
    </div>
    <div>
      <h2>Модальное окно создания упражнения</h2>
      <button @click="openModal3">Создать упражнение</button>
      <CreateExerciseWindow :isVisible="isModalVisible3" :keyboardZones="keyboardZones" :minCount="minCount"
        :numberErrors="5" :timePressKey="pressTime" :maxCount="maxCount" @update:isVisible="isModalVisible3 = $event" />
    </div>
    <div>
      <h2>Модальное окно изменения упражнения</h2>
      <button @click="openModal4">Изменить упражнение</button>
      <EditExerciseWindow :text-exercise="textExercise" :isVisible="isModalVisible4" :keyboardZones="keyboardZones"
        :minCount="minCount" :numberErrors="5" :timePressKey="pressTime" :maxCount="maxCount"
        @update:isVisible="isModalVisible4 = $event" />
    </div>
    <div>
      <h2>Клавиатура</h2>
      <div>
        <Keyboard class="keyboard" :currentCharacter="currentCharacter" />
      </div>
    </div>
    <div>
      <h2>Таблица</h2>
      <BaseTable :headers="tableHeaders" :data="tableData" custom-style="width: 700px;" />
    </div>
    <div>
      <h2>Гистограммы</h2>
      <div>
        <h1>Накопленная гистограмма</h1>

        <!-- <StackedBarChart :data="chartData" /> -->
      </div>
    </div>
  </main>
</template>
