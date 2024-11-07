<template>
    <button 
        class="baseButtonBody baseButtonText" 
        :style="computedStyles"
    >
        <slot></slot>
    </button>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  props: {
    width: {
      type: String,
      default: 'auto'
    },
    height: {
      type: String,
      default: 'auto'
    }
  },
  setup(props) {
    const computedStyles = computed(() => ({
      width: props.width,
      height: props.height,
    }));

    return {
      computedStyles
    };
  }
});
</script>

<style scoped>
.baseButtonBody {
    border-radius: 15px;
    border: none; /* Убедитесь, что граница отсутствует */
    background-color: #81BECE;
    opacity: 0.8;
    padding: 10px 20px; /* Добавлено внутреннее поле для улучшения внешнего вида */
    cursor: pointer; /* Указатель при наведении */
    transition: background-color 0.3s, opacity 0.3s, transform 0.1s; /* Плавный переход для эффектов */
}

.baseButtonBody:hover {
    background-color: #6FA1B6; /* Изменение цвета фона при наведении */
    opacity: 1; /* Полная непрозрачность при наведении */
}

.baseButtonBody:active {
    background-color: #5B8DA1; /* Цвет фона при нажатии */
    transform: scale(0.95); /* Уменьшение размера кнопки при нажатии */
    opacity: 0.9; /* Немного уменьшенная непрозрачность при нажатии */
}

.baseButtonText {
    text-align: center;
    color: #012e4a;
    font-family: "Alegreya Sans SC", sans-serif; /* Шрифт */
}
</style>
