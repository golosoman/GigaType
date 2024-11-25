<template>
    <div>
        <CheckBoxGroupWithBlock :options="checkOptions" :valuesSelected="selectedOptions"
            @update:selectedValues="handleSelectedValues" :columns="3" customStyle="width: 570px"
            customStyleForBaseCheckbox="margin-bottom: 10px;"></CheckBoxGroupWithBlock>
        <KeybordForZones :selectedZones="selectedOptions" custom-style="margin-top: 20px" />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { CheckBoxGroupWithBlock } from '@/component/UI';
import { KeybordForZones } from '../keyboard';
import { KeyboardZones } from '../util';

export default defineComponent({
    name: 'App',
    components: {
        CheckBoxGroupWithBlock,
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
