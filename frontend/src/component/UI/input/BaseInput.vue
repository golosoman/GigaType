<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
    name: 'BaseInput',
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
        customStyle: {
            type: String,
            default: ''
        },
        id: {
            type: String,
            default: ''
        }
    },
    emits: ['update:modelValue'],
    setup(props, { emit }) {
        const inputValue = ref(props.modelValue);

        watch(() => props.modelValue, (newValue) => {
            inputValue.value = newValue; // Обновляем локальное состояние
        });

        const updateInput = (event: Event) => {
            const target = event.target as HTMLInputElement;
            inputValue.value = target.value; // Обновляем локальное состояние
            emit('update:modelValue', target.value); // Эмитируем новое значение
        };

        return { inputValue, updateInput };
    }
});
</script>

<template>
    <input :value="inputValue" @input="updateInput" class="baseInputBody baseInputText" :id="id" :type="inputType"
        :placeholder="inputPlaceholder" :style="customStyle" />
</template>

<style scoped>
input[type='number']::-webkit-inner-spin-button,
input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.baseInputBody {
    border-radius: 15px;
    border: none;
    background-color: #81BECE;
    outline: none;
    padding-left: 10px;
    transition: box-shadow 0.3s ease;
}

.baseInputBody:focus {
    box-shadow: 0 0 5px #012e4a88;
}

.baseInputText {
    font-family: "Alegreya Sans SC";
    color: #012e4a;
    border: none;
    width: 100%;
    outline: none;
}

.baseInputText::placeholder {
    color: #012e4a88;
}

.baseInputText:focus {
    color: #012e4a;
}
</style>
