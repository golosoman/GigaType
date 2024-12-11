<template>
    <BaseCheckboxGroup :options="checkOptions" :columns="3" customStyle="width: 570px"
        @update:selectedValues="handleSelectedValues" :values-selected="selectedOptions" />
    <KeybordForZones :selectedZones="selectedOptions" custom-style="margin-top: 20px" />
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { BaseCheckboxGroup } from '@/component/UI';
import { KeybordForZones } from '../keyboard';
import { KeyboardZones } from '../util';

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
            KeyboardZones.ZONE_1,
            KeyboardZones.ZONE_2,
            KeyboardZones.ZONE_3,
            KeyboardZones.ZONE_4,
            KeyboardZones.ZONE_5,
            KeyboardZones.ZONE_6,
            KeyboardZones.ZONE_7,
            KeyboardZones.ZONE_8,
            KeyboardZones.ZONE_9
        ];

        const handleSelectedValues = (values: string[]) => {
            selectedOptions.value = values;
            console.log(`Появились изменения ${values}`)
            // console.log(`Появились изменения ${selectedOptions.value}`)
            emit('update:selectedValues', selectedOptions.value);
        };

        // Слежение за изменением пропса selectedZones
        watch(() => props.keyboardZones, (newZones) => {
            selectedOptions.value = newZones
            console.log(`Зоны изменились! ${newZones}`);
        });

        return {
            selectedOptions,
            checkOptions,
            handleSelectedValues,
        };
    },
});
</script>
