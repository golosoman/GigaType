<template>
    <div class="text-container" :style="customStyle">
        <div class="input-text">{{ visibleInputText }}</div>
        <div class="text-to-type">{{ visibleTextToType }}</div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, computed } from 'vue';

export default defineComponent({
    name: 'TypingTrainer',
    props: {
        textToType: {
            type: String,
            required: true,
        },
        customStyle: {
            type: String,
            required: false,
            default: ''
        },
    },
    setup(props, { emit }) {
        const inputText = ref<string>(''); // текст, который пользователь ввел
        const textToType = ref<string>(props.textToType); // текст, который нужно ввести

        const handleKeydown = (event: KeyboardEvent) => {
            const nextChar = textToType.value[0]; // первый символ текста, который нужно ввести
            if (event.key === nextChar) {
                inputText.value += event.key; // добавляем символ в введенный текст
                textToType.value = textToType.value.slice(1); // удаляем символ из текста, который нужно ввести
            } else if (event.key === 'Backspace') {
                // Удаление текста запрещено, просто игнорируем нажатие Backspace
                event.preventDefault();
            } else {
                // Отменяем ввод, если символ неверный
                event.preventDefault();
            }
            // Проверка завершения ввода
            if (textToType.value.length === 0) {
                emit('completed', inputText.value); // Генерируем событие при завершении ввода
                console.log('Вы ввели текст правильно!');
                // Удаляем слушатель событий, так как ввод завершен
                window.removeEventListener('keydown', handleKeydown);
            }
        };

        onMounted(() => {
            window.addEventListener('keydown', handleKeydown); // Добавляем слушатель событий при монтировании
        });

        onBeforeUnmount(() => {
            window.removeEventListener('keydown', handleKeydown); // Удаляем слушатель событий при размонтировании
        });

        const visibleTextToType = computed(() => {
            return textToType.value;
        });

        const visibleInputText = computed(() => {
            return inputText.value;
        });

        return {
            visibleTextToType,
            visibleInputText,
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
    text-overflow: ellipsis;
    flex: 1;
}

.input-text {
    color: black;
    white-space: pre;
    text-align: right;
    display: flex;
    justify-content: flex-end;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}
</style>
