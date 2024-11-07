<script lang="ts">
import { defineComponent, ref } from 'vue';
import BaseInput from './BaseInput.vue'; // Убедитесь, что путь к вашему компоненту верный
import { setUniqId } from './util';
export default defineComponent({
    components: {
        BaseInput
    },
    props: {
        modelValue: {
            type: [String, Number],
            required: true,
        },
        inputPlaceholder: {
            type: String,
            default: 'Ввод: '
        },
        inputType: {
            type: String,
            default: 'text'
        },
        inputWidth: {
            type: String,
            default: 'auto'
        },
        inputHeight: {
            type: String,
            default: 'auto'
        },
        label: {
            type: String,
            required: true,
        },
    },
    setup() {
        const inputId = setUniqId(); // Генерируем уникальный id для label и input
        return { inputId };
    }
});
</script>
<template>
    <div class="inputWithLabel">
        <label :for="inputId" class="label">{{ label }}</label>
        <BaseInput
            v-model="modelValue"
            :inputPlaceholder="inputPlaceholder"
            :inputType="inputType"
            :width="inputWidth"
            :height="inputHeight"
            :id="inputId"
        />
    </div>
</template>
<style scoped>
.inputWithLabel {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem; /* Отступ между полями ввода */
}
.label {
    font-family: "Alegreya Sans SC", sans-serif; /* Шрифт для метки */
    color: #012E4A; /* Цвет текста метки */
    margin-bottom: 0.5rem; /* Отступ между меткой и полем ввода */
}
</style>
