<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div>
                Создание уровня сложности
            </div>
            <KeyboardWithBlockCheckBox :keyboardZones="zoneKeyboard" />
            <div style="display: flex;">
                <div>
                    <BaseInput inputPlaceholder="Поле минимального количества символов:" :modelValue="minCountChar"
                        :disabled="true"
                        customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                        customStyleForLabel="font-size: 32px;" />
                    <BaseInput inputPlaceholder="Поле максимального количества символов" :modelValue="maxCountChar"
                        :disabled="true"
                        customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                        customStyleForLabel="font-size: 32px;" />
                    <BaseInput inputPlaceholder="Поле допустимого окличества ошибок" :modelValue="numberErrors"
                        :disabled="true"
                        customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                        customStyleForLabel="font-size: 32px;" />
                    <BaseInput inputPlaceholder="Поле времени нажатия на клавишу" :modelValue="timePressKey"
                        :disabled="true"
                        customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                        customStyleForLabel="font-size: 32px;" />
                </div>

                <div style="margin-left: 20px;">
                    <BaseInput inputPlaceholder="Введите количество символов для генерации:"
                        :modelValue="lengthExercise" @update:modelValue="changeLengthExercise"
                        customStyleForInput="width: 732px; height: 57px; font-size: 32px; background-color: #B7BBBC;"
                        customStyleForLabel="font-size: 32px;" />
                    <BaseButton>Генерация упражнения</BaseButton>
                </div>
            </div>
            <BaseInputTextArea :modelValue="textExercise" @update:modelValue="changeTextExercise" />
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
import { KeyboardWithBlockCheckBox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage, BaseInput, BaseInputTextArea } from '@/component/UI';
import CloseUrl from '@/assets/Close.png';

export default defineComponent({
    name: 'EditExerciseWindow',
    components: {
        KeyboardWithBlockCheckBox,
        BaseInputWithLabel,
        BaseInput,
        BaseButton,
        ButtonWithImage,
        BaseInputTextArea
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
        numberErrors: {
            type: Number,
            required: true,
        },
        timePressKey: {
            type: Number,
            required: true,
        },
        textExercise: {
            type: String,
            required: true,
        }
    },
    setup(props, { emit }) {
        const minCountChar = ref(`Минимальное количество символов - ${props.minCount}`);
        const maxCountChar = ref(`Максимальное количество символов - ${props.maxCount}`);
        const timePressKey = ref(`Время нажатия на клавишу - ${props.timePressKey}`);
        const numberErrors = ref(`Допустимое количество ошибок - ${props.numberErrors}`);
        const textExercise = ref(props.textExercise)
        const zoneKeyboard = ref(props.keyboardZones);
        const lengthExercise = ref<number | string>('')

        const changeTextExercise = (value: string) => {
            textExercise.value = value
        }

        const changeLengthExercise = (value: number) => {
            lengthExercise.value = value
        }

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
            textExercise,
            minCountChar,
            maxCountChar,
            timePressKey,
            CloseUrl,
            zoneKeyboard,
            numberErrors,
            lengthExercise,
            changeTextExercise,
            changeLengthExercise,
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