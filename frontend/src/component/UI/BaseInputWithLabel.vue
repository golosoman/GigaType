<script lang="ts">
import { defineComponent } from 'vue';
import BaseInput from './BaseInput.vue';
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
        customStyleForInput: {
            type: String,
            default: ''
        },
        customStyleForLabel: {
            type: String,
            default: ''
        },
        label: {
            type: String,
            required: true,
        },
    },
    emits: ['update:modelValue'],
    setup(props, { emit }) {
        const inputId = setUniqId();

        const updateValue = (value: string) => {
            emit('update:modelValue', value); // Эмитируем обновление
        };

        return { inputId, updateValue };
    }
});
</script>

<template>
    <div class="inputWithLabel">
        <label :for="inputId" class="label" :style="customStyleForLabel">{{ label }}</label>
        <BaseInput :modelValue="modelValue" @update:modelValue="updateValue" :inputPlaceholder="inputPlaceholder"
            :inputType="inputType" :customStyle="customStyleForInput" :id="inputId" />
        <!-- Обработка события -->
    </div>
</template>


<style scoped>
.inputWithLabel {
    display: flex;
    flex-direction: column;
}

.label {
    font-family: "Alegreya Sans SC";
    color: #012E4A;
}
</style>
