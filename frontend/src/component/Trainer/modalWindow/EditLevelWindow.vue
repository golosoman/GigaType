<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div>
                Создание уровня сложности
            </div>
            <KeyboardWithCheckbox :keyboardZones="zoneKeyboard" />
            <BaseInputWithLabel label="Минимальное количество символов"
                inputPlaceholder="Введите минимальное количество символов:" :modelValue="minCountChar"
                @update:modelValue="changeMinCountChar"
                customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 32px;" />
            <BaseInputWithLabel label="Максимальное количество символов"
                inputPlaceholder="Введите максимальное количество символов:" :modelValue="maxCountChar"
                @update:modelValue="changeMaxCountChar"
                customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 32px;" />
            <BaseInputWithLabel label="Время нажатия на клавишу" inputPlaceholder="Введите время нажатия на клавишу:"
                :modelValue="timePressKey" @update:modelValue="changeTimePressKey"
                customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 32px;" />
            <BaseButton
                customStyle="width: 171px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;"
                @click="saveChanges">
                Сохранить
            </BaseButton>
            <ButtonWithImage class="close-button" @click="closeModal" :imageSrc="CloseUrl"
                customStyle="background-color: #D9D9D9;" customStyleForImage="width: 30px; height: 30px;">
            </ButtonWithImage>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { KeyboardWithCheckbox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import CloseUrl from '@/assets/Close.png';

export default defineComponent({
    name: 'EditLevelWindow',
    components: {
        KeyboardWithCheckbox,
        BaseInputWithLabel,
        BaseButton,
        ButtonWithImage
    },
    props: {
        isVisible: {
            type: Boolean,
            required: true,
        },
        keyboardZones: {
            type: Array as () => string[],
            required: true,
        },
        minCount: {
            type: Number,
            required: true,
        },
        maxCount: {
            type: Number,
            required: true,
        },
        timePressKey: {
            type: Number,
            required: true,
        }
    },
    setup(props, { emit }) {
        const minCountChar = ref(props.minCount);
        const maxCountChar = ref(props.maxCount);
        const timePressKey = ref(props.timePressKey);
        const zoneKeyboard = ref(props.keyboardZones);
        const changeMinCountChar = (value: number) => {
            minCountChar.value = value;
        };

        const changeMaxCountChar = (value: number) => {
            maxCountChar.value = value;
        };

        const changeTimePressKey = (value: number) => {
            timePressKey.value = value;
        };

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const saveChanges = () => {
            // Здесь вы можете обработать сохранение изменений
            console.log('Сохраненные значения:', {
                minCount: minCountChar.value,
                maxCount: maxCountChar.value,
                timePressKey: timePressKey.value,
            });
            closeModal();
        };

        return {
            minCountChar,
            maxCountChar,
            timePressKey,
            CloseUrl,
            zoneKeyboard,
            changeMinCountChar,
            changeMaxCountChar,
            changeTimePressKey,
            closeModal,
            saveChanges,
        };
    },
});
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 3;
}

.modal-content {
    background: #D9D9D9;
    padding: 20px;
    border-radius: 5px;
    position: relative;
    max-width: 70%;
    width: 100%;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    border: none;
    background: none;
    cursor: pointer;
    font-size: 20px;
}
</style>