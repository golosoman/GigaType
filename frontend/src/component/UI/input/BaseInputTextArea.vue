<template>
    <div class="text-area-container" :style="customStyle">
        <textarea v-model="text" @input="updateInput" class="text-area" :placeholder="inputPlaceholder"
            rows="5"></textarea>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
    name: 'TextAreaComponent',
    props: {
        modelValue: {
            type: String,
            required: true,
        },
        inputPlaceholder: {
            type: String,
            default: 'Введите ваш текст здесь...',
        },
        customStyle: {
            type: String,
            default: '',
        },
        allowedCharacters: {
            type: String,
            required: true, // Новое свойство для разрешенных символов
        },
    },
    setup(props, { emit }) {
        const text = ref<string>(props.modelValue);

        // Наблюдатель за изменением пропса modelValue
        watch(() => props.modelValue, (newValue) => {
            text.value = newValue;
        });

        const updateInput = (event: Event) => {
            const target = event.target as HTMLTextAreaElement;
            const inputValue = target.value;

            // Фильтрация вводимых символов независимо от регистра
            const filteredValue = inputValue
                .split('')
                .filter(char => props.allowedCharacters.toLowerCase().includes(char.toLowerCase()))
                .join('');

            text.value = filteredValue;
            emit('update:modelValue', filteredValue);
        };

        return {
            text,
            updateInput,
        };
    },
});
</script>

<style scoped>
.text-area-container {
    display: flex;
    flex-direction: column;
    margin: 20px;
}

.text-area {
    width: 100%;
    font-size: 16px;
    padding: 10px;
    border: 1px solid #ccc;
    border-color: #B7BBBC;
    background-color: #B7BBBC;
    border-radius: 4px;
    resize: vertical;
}
</style>
