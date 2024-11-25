<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div>
                Создание уровня сложности
            </div>
            <KeyboardWithCheckbox></KeyboardWithCheckbox>
            <BaseInputWithLabel label="Минимальное количество символов"
                inputPlaceholder="Введите минимальное количество символов:" :modelValue="min_count_char"
                @update:modelValue="changeMinCountChar"
                customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 32px;" />
            <BaseInputWithLabel label="Максимальное количество символов"
                inputPlaceholder="Введите максимальное количество символов:" :modelValue="max_count_char"
                @update:modelValue="changeMaxCountChar"
                customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 32px;" />
            <BaseInputWithLabel label="Время нажатия на клавишу" inputPlaceholder="Введите время нажатия на клавишу:"
                :modelValue="time_press_key" @update:modelValue="changeTimePressKey"
                customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 32px;" />
            <BaseButton
                customStyle="width: 171px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
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
import { KeyboardWithCheckbox } from '../editor';
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import CloseUrl from '@/assets/Close.png'
export default defineComponent({
    name: 'CreateLevelWindow',
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
    },
    setup(props, { emit }) {
        const min_count_char = ref('')
        const changeMinCountChar = () => {

        }

        const max_count_char = ref('')
        const changeMaxCountChar = () => {

        }

        const time_press_key = ref('')
        const changeTimePressKey = () => {

        }

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        return {
            min_count_char,
            max_count_char,
            time_press_key,
            CloseUrl,
            changeTimePressKey,
            changeMaxCountChar,
            changeMinCountChar,
            closeModal,
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