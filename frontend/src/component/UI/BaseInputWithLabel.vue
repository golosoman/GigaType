<script lang="ts">
import { defineComponent } from 'vue';
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
        customStyleForInput: { // Новый пропс для стилей поля ввода
            type: String,
            default: ''
        },
        customStyleForLabel: { // Новый пропс для стилей метки
            type: String,
            default: ''
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
        <label :for="inputId" class="label" :style="customStyleForLabel">{{ label }}</label>
        <BaseInput v-model="modelValue" :inputPlaceholder="inputPlaceholder" :inputType="inputType"
            :customStyle="customStyleForInput" :id="inputId" />
    </div>
</template>
<style scoped>
.inputWithLabel {
    display: flex;
    flex-direction: column;
}

.label {
    font-family: "Alegreya Sans SC";
    /* Шрифт для метки */
    color: #012E4A;
    /* Цвет текста метки */
}
</style>
