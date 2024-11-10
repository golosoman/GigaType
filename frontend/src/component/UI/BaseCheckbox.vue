<template>
    <label :style="customStyle" class="checkbox-container">
        <input type="checkbox" :checked="modelValue" @change="toggleCheckbox" />
        <span class="checkmark"></span>
        {{ label }}
    </label>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'BaseCheckbox',
    props: {
        modelValue: {
            type: Boolean,
            default: false,
        },
        customStyle: {
            type: String,
            required: false,
            default: ''
        },
        label: {
            type: String,
            required: true,
        },
    },
    emits: ['update:modelValue'],
    methods: {
        toggleCheckbox(event: Event) {
            const checked = (event.target as HTMLInputElement).checked;
            this.$emit('update:modelValue', checked);
        },
    },
});
</script>

<style scoped>
.checkbox-container {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.checkbox-container input {
    display: none;
}

.checkmark {
    width: 20px;
    height: 20px;
    border: 2px solid #4c8a9a;
    border-radius: 4px;
    margin-right: 10px;
    position: relative;
}

.checkbox-container input:checked+.checkmark {
    background-color: #81BECE;
}

.checkbox-container input:checked+.checkmark::after {
    content: '';
    position: absolute;
    left: 7px;
    top: 2px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
}
</style>
