<template>
    <div class="text-area-container" :style="customStyle">
        <textarea v-model="text" @input="updateInput" class="text-area" :placeholder="inputPlaceholder"
            rows="5"></textarea>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'TextAreaComponent',
    props: {
        modelValue: {
            type: String,
            required: true,
        },
        inputPlaceholder: {
            type: String,
            default: 'Введите ваш текст здесь...'
        },
        customStyle: {
            type: String,
            default: ''
        },
    },
    setup(props, { emit }) {
        const text = ref<string>(props.modelValue);

        const updateInput = (event: Event) => {
            const target = event.target as HTMLInputElement;
            text.value = target.value;
            emit('update:modelValue', target.value);
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
    border-radius: 4px;
    resize: vertical;
    /* Позволяет изменять размер по вертикали */
}

.text-preview {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f9f9f9;
    white-space: pre-wrap;
    /* Сохраняет пробелы и переносы строк */
}
</style>