<template>
    <div class="text-container" :style="customStyle">
        <div class="input-text">{{ visibleInputText }}</div>
        <div class="text-to-type">{{ visibleTextToType }}</div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, computed, watch } from 'vue';

export default defineComponent({
    name: 'TrainingField',
    props: {
        textToType: {
            type: String,
            required: true,
        },
        customStyle: {
            type: String,
            default: ''
        },
        inputControl: {
            type: Boolean,
            default: true
        },
        modelValue: { // Изменено на modelValue для v-model
            type: String,
            default: ''
        },
    },
    setup(props, { emit }) {
        const inputText = ref<string>(props.modelValue);

        // Смотрите за изменениями modelValue и обновляйте inputText
        watch(() => props.modelValue, (newValue) => {
            inputText.value = newValue;
        });

        const specialKeys = new Set([
            'Backspace', 'Tab', 'Enter', 'Shift', 'Control', 'Alt', 'Meta',
            'CapsLock', 'Escape', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
            'Insert', 'Delete', 'Home', 'End', 'PageUp', 'PageDown', 'PrintScreen',
            'ScrollLock', 'Pause', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7',
            'F8', 'F9', 'F10', 'F11', 'F12'
        ]);

        const visibleTextToType = computed(() => props.textToType.slice(inputText.value.length));
        const visibleInputText = computed(() => inputText.value);

        const handleKeydown = (event: KeyboardEvent) => {
            if (!props.inputControl) return;

            const nextChar = visibleTextToType.value[0];
            if (event.key === nextChar) {
                inputText.value += event.key;
                emit('update:modelValue', inputText.value); // Эмитим обновление
                emit('right-character', inputText.value);
            } else if (specialKeys.has(event.key)) {
                event.preventDefault();
            } else {
                emit('invalid-character', event.key);
                event.preventDefault();
            }

            if (visibleTextToType.value.length === 0) {
                emit('completed', inputText.value);
                console.log('Вы ввели текст правильно!');
            }
        };

        onMounted(() => {
            window.addEventListener('keydown', handleKeydown);
        });

        onBeforeUnmount(() => {
            window.removeEventListener('keydown', handleKeydown);
        });

        const reset = () => {
            inputText.value = '';
            emit('update:modelValue', ''); // Сбрасываем значение в родительском компоненте
        };

        return {
            visibleTextToType,
            visibleInputText,
            reset,
        };
    },
});
</script>

<style scoped>
.text-container {
    font-family: "Alegreya Sans SC";
    display: flex;
    flex-direction: row;
    align-items: center;
    background-color: #81BECE;
    overflow: hidden;
}

.text-to-type {
    color: gray;
    white-space: pre;
    overflow: hidden;
    /* text-overflow: ellipsis; */
    /* Убрано многоточие */
    flex: 1;
}

.input-text {
    color: black;
    white-space: pre;
    text-align: right;
    display: flex;
    justify-content: flex-end;
    overflow: hidden;
    /* text-overflow: ellipsis; */
    /* Убрано многоточие */
    flex: 1;
}
</style>
