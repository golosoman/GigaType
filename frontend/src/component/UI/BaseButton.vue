<template>
  <button :style="customStyle" class="baseButtonBody baseButtonText">
    <slot></slot> <!-- Слот для передачи содержимого кнопки -->
  </button>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'CustomButton',
  props: {
    customStyle: {
      type: String,
      required: false,
      default: ''
    }
  }
});
</script>

<style scoped>
.baseButtonBody {
  border: none;
  /* Убираем границу */
  background-color: #81BECE;
  opacity: 0.8;
  /* Добавлено внутреннее поле для улучшения внешнего вида */
  cursor: pointer;
  /* Указатель при наведении */
  transition: background-color 0.3s, opacity 0.3s, transform 0.1s;
  /* Плавный переход для эффектов */
}

.baseButtonBody:hover {
  background-color: #6FA1B6;
  /* Изменение цвета фона при наведении */
  opacity: 1;
  /* Полная непрозрачность при наведении */
}

.baseButtonBody:active {
  background-color: #5B8DA1;
  /* Цвет фона при нажатии */
  transform: scale(0.95);
  /* Уменьшение размера кнопки при нажатии */
  opacity: 0.9;
  /* Немного уменьшенная непрозрачность при нажатии */
}

.baseButtonText {
  color: #012e4a;
  font-family: "Alegreya Sans SC";
  /* Шрифт */
}
</style>
