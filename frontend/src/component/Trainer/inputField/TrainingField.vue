<template>
    <div class="text-container" :style="customStyle">
        <div class="input-text">{{ inputText }}</div>
        <div class="text-to-type">{{ visibleTextToType }}</div>
        <div class="overlay-text">{{ textPreview }}</div>
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
        inputText: {
            type: String,
            default: ''
        },
        textPreview: {
            type: String,
            default: ''
        }
    },
    setup(props, { emit }) {
        const inputText = ref<string>('');
        const nextChar = ref('');
        const textPreview = ref(props.textPreview);

        watch(() => props.inputText, (newValue) => {
            inputText.value = newValue;
        });

        emit('update:inputText', inputText.value);

        watch(() => props.textPreview, (newValue) => {
            textPreview.value = newValue;
        });

        const specialKeys = new Set([
            'Backspace', 'Tab', 'Enter', 'Shift', 'Control', 'Alt', 'Meta',
            'CapsLock', 'Escape', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
            'Insert', 'Delete', 'Home', 'End', 'PageUp', 'PageDown', 'PrintScreen',
            'ScrollLock', 'Pause', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7',
            'F8', 'F9', 'F10', 'F11', 'F12'
        ]);


        const visibleTextToType = computed(() => props.textToType.slice(inputText.value.length));
        emit('current-charrecter', visibleTextToType.value[0])

        const handleKeydown = (event: KeyboardEvent) => {
            if (!props.inputControl) return;
            nextChar.value = visibleTextToType.value[0];

            if (event.key === nextChar.value) {
                if (visibleTextToType.value.length > 1) {
                    emit('current-charrecter', visibleTextToType.value[1])
                }
                else {
                    emit('current-charrecter', '')
                }
                inputText.value += event.key;
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

        return {
            visibleTextToType,
            nextChar,
            textPreview,
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
    position: relative;
}

.text-to-type {
    color: gray;
    white-space: pre;
    overflow: hidden;
    flex: 1;
}

.input-text {
    color: black;
    white-space: pre;
    text-align: right;
    display: flex;
    justify-content: flex-end;
    overflow: hidden;
    flex: 1;
    position: relative;
    z-index: 1;
}

.overlay-text {
    position: absolute;
    top: 30%;
    left: 0;
    width: 50%;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    color: black;
    pointer-events: none;
    font-size: inherit;
    z-index: 2;
}
</style>