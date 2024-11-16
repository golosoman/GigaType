<template>
    <div :style="[gridStyle, customStyle]" class="checkbox-group">
        <BaseCheckbox v-for="(option, index) in options" :key="index" :modelValue="selectedValues.includes(option)"
            :label="option" @update:modelValue="(value) => updateCheckboxValue(option, value)"
            :customStyle="customStyleForBaseCheckbox" />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import BaseCheckbox from './BaseCheckbox.vue';

export default defineComponent({
    name: 'BaseCheckboxGroup',
    components: {
        BaseCheckbox,
    },
    props: {
        options: {
            type: Array as () => string[],
            required: true,
        },
        columns: {
            type: Number,
            default: 2,
        },
        customStyle: {
            type: String,
            required: false,
            default: ''
        },
        customStyleForBaseCheckbox: {
            type: String,
            required: false,
            default: ''
        },
    },
    setup(props, { emit }) {
        const selectedValues = ref<string[]>([]);

        const updateCheckboxValue = (option: string, checked: boolean) => {
            if (checked) {
                selectedValues.value.push(option);
            } else {
                selectedValues.value = selectedValues.value.filter(value => value !== option);
            }
            emit('update:selectedValues', selectedValues.value);
        };

        // Вычисляемое свойство для стиля сетки
        const gridStyle = computed(() => ({
            display: 'grid',
            gridTemplateColumns: `repeat(${props.columns}, 1fr)`, // Устанавливаем количество колонок
            gap: '10px', // Отступы между чекбоксами
        }));

        return {
            selectedValues,
            updateCheckboxValue,
            gridStyle,
        };
    },
});
</script>

<style scoped>
.checkbox-group>div {
    display: flex;
    align-items: center;
}
</style>
