<template>
    <div class="dropdown" :style="customStyle">
        <button class="dropdown-toggle" @click="toggleDropdown">
            {{ selectedOption?.label || placeholder }} ▼
        </button>
        <div v-if="isOpen" class="dropdown-menu">
            <div v-for="option in options" :key="option.value" class="dropdown-item" @click="selectOption(option)">
                {{ option.label }}
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
    name: 'BaseDropdown',
    props: {
        modelValue: {
            type: Object as () => { label: string; value: string } | null | undefined,
            default: null,
        },
        options: {
            type: Array as () => Array<{ label: string; value: string }>,
            required: true,
        },
        placeholder: {
            type: String,
            default: 'Выберите опцию',
        },
        customStyle: {
            type: String,
            required: false,
            default: ''
        },
    },
    setup(props, { emit }) {
        const isOpen = ref(false);
        const selectedOption = ref<{ label: string; value: string } | null | undefined>(props.modelValue);

        const toggleDropdown = () => {
            isOpen.value = !isOpen.value;
        };

        const selectOption = (option: { label: string; value: string }) => {
            selectedOption.value = option;
            isOpen.value = false;
            emit('update:modelValue', option); // Эмитируем весь объект option
        };

        // Слежение за изменением props.modelValue
        watch(() => props.modelValue, (newValue) => {

            selectedOption.value = newValue;
        });

        return {
            isOpen,
            selectedOption,
            toggleDropdown,
            selectOption,
        };
    },
});
</script>

<style scoped>
.dropdown {
    position: relative;
    display: inline-block;
    font-family: "Alegreya Sans SC";
    font-size: 16px;
}

.dropdown-toggle {
    padding: 10px;
    cursor: pointer;
    border: none;
    background-color: #81BECE;
    transition: background-color 0.3s, opacity 0.3s, transform 0.1s;
    border-radius: 10px;
}

.dropdown-toggle:active {
    transform: scale(0.95);
    opacity: 0.9;
}

.dropdown-toggle:hover {
    background-color: #6FA1B6;
}

.dropdown-menu {
    position: absolute;
    background-color: #81BECE;
    border: none;
    margin-top: 1px;
    z-index: 1;
    width: 100%;
    border-radius: 10px;
}

.dropdown-item {
    padding: 10px;
    cursor: pointer;
}

.dropdown-item:hover {
    background-color: #6FA1B6;
    border-radius: 10px;
}
</style>