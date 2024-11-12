<template>
  <button :style="customStyle" class="baseButtonBody baseButtonText">
    <slot></slot>
  </button>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'BaseButton',
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
  background-color: #81BECE;
  opacity: 0.8;
  cursor: pointer;
  transition: background-color 0.3s, opacity 0.3s, transform 0.1s;
}

.baseButtonBody:hover {
  background-color: #6FA1B6;
  opacity: 1;
}

.baseButtonBody:active {
  background-color: #5B8DA1;
  transform: scale(0.95);
  opacity: 0.9;
}

.baseButtonText {
  color: #012e4a;
  font-family: "Alegreya Sans SC";
}
</style>
