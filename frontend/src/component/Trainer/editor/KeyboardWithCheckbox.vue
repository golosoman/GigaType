<template>
    <div>
        <BaseCheckboxGroup :options="checkOptions" :columns="3" customStyle="width: 570px"
            @update:selectedValues="handleSelectedValues" :values-selected="selectedOptions" />
        <KeybordForZones :selectedZones="selectedOptions" custom-style="margin-top: 20px" />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { BaseCheckboxGroup } from '@/component/UI';
import { KeybordForZones } from '../keyboard';

export default defineComponent({
    name: 'App',
    components: {
        BaseCheckboxGroup,
        KeybordForZones,
    },
    props: {
        keyboardZones: {
            type: Array<string>,
            required: false,
            default: []
        },
    },
    setup(props, { emit }) {
        const selectedOptions = ref<string[]>(props.keyboardZones);
        const checkOptions = [
            'Зона 1 (ФЫВАОЛДЖ)',
            'Зона 2 (ПР)',
            'Зона 3 (КЕНГ)',
            'Зона 4 (МИТЬ)',
            'Зона 5 (УСШБ)',
            'Зона 6 (ЦЧЩЮ)',
            'Зона 7 (ЁЙЯЗХЪЭ.,)',
            'Зона 8 (1234567890)',
            'Зона 9 (символы)'
        ];

        const handleSelectedValues = (values: string[]) => {
            selectedOptions.value = values;
            console.log(`Появились изменения ${values}`)
            emit('update:selectedValues', selectedOptions.value);
        };

        return {
            selectedOptions,
            checkOptions,
            handleSelectedValues,
        };
    },
});
</script>
