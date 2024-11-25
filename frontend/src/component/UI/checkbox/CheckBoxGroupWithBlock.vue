<template>
    <div :style="[gridStyle, customStyle]" class="checkbox-group">
        <BaseCheckbox v-for="(option, index) in options" :key="index" :modelValue="selectedValues.includes(option)"
            :label="option" @update:modelValue="(value) => updateCheckboxValue(option, value)"
            :customStyle="customStyleForBaseCheckbox" :disabled_property="!activValues.includes(option)"
            :class="{ 'disabled-checkbox': !activValues.includes(option) }" />
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
        valuesSelected: {
            type: Array as () => string[],
            required: false,
            default: () => []
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
        const activValues = ref<string[]>(props.valuesSelected);
        const selectedValues = ref<string[]>(props.valuesSelected);

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
            activValues,
            selectedValues,
            updateCheckboxValue,
            gridStyle,
        };
    },
});
</script>

<style scoped>
.checkbox-group {
    display: flex;
    flex-wrap: wrap;
}

.disabled-checkbox {
    /* Цвет фона для неактивных чекбоксов */
    opacity: 0.5;
    /* Прозрачность для визуального эффекта */
    pointer-events: none;
    /* Отключение взаимодействия */
}
</style>