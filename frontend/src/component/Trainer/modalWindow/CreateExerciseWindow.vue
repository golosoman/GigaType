<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Создание уровня сложности
            </div>
            <KeyboardWithBlockCheckBox @update:selectedOptions="handleSelectedValues" :keyboardZones="keyboardZones" />
            <div style="display: flex;">
                <div style="width:400px;">
                    <BaseInput inputPlaceholder="Поле минимального количества символов:"
                        :modelValue="`Минимальное количество символов - ${minCount}`" :disabled="true"
                        customStyle="width: 400px; height: 30px; font-size: 20px; background-color: #B7BBBC;" />
                    <BaseInput inputPlaceholder="Поле максимального количества символов"
                        :modelValue="`Максимальное количество символов - ${maxCount}`" :disabled="true"
                        customStyle="width: 400px; height: 30px; font-size: 20px; background-color: #B7BBBC; margin-top: 10px;" />
                    <BaseInput inputPlaceholder="Поле допустимого количества ошибок"
                        :modelValue="`Допустимое количество ошибок - ${numberErrors}`" :disabled="true"
                        customStyle="width: 400px; height: 30px; font-size: 20px; background-color: #B7BBBC; margin-top: 10px;" />
                    <BaseInput inputPlaceholder="Поле времени нажатия на клавишу"
                        :modelValue="`Время нажатия на клавишу - ${timePressKey}`" :disabled="true"
                        customStyle="width: 400px; height: 30px; font-size: 20px; background-color: #B7BBBC; margin-top: 10px;" />
                </div>

                <div style="display: flex; flex-direction: column; align-items: center; margin: auto 20px;">
                    <BaseInput inputPlaceholder="Введите количество символов для генерации:"
                        :modelValue="lengthExercise" @update:modelValue="changeLengthExercise"
                        customStyle="width: 400px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                        inputType="number" />
                    <BaseButton
                        customStyle="width: 250px; height: 30px; font-size: 20px; border-radius: 15px; margin-top: 10px; color: #012E4A;">
                        Генерация упражнения
                    </BaseButton>
                </div>
            </div>
            <BaseInputTextArea v-model="textExercise" @update:modelValue="changeTextExercise"
                inputPlaceholder="Введите текст упражнения:" :allowedCharacters="getAllowedCharacters(keyboardZones)" />
            <BaseButton
                customStyle="width: 150px; height: 30px; font-size: 20px; border-radius: 15px; margin-top: 41px; color: #012E4A;"
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
import axios from 'axios'; // Импортируем Axios
import { KeyboardWithBlockCheckBox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage, BaseInput, BaseInputTextArea } from '@/component/UI';
import { getZoneNameFromSelectedOptions } from '@/component/Trainer/modalWindow';
import CloseUrl from '@/assets/Close.png';

export default defineComponent({
    name: 'CreateExerciseWindow',
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
        difficultyId: {
            type: String,
            required: false, // или уберите это, если хотите сделать его необязательным
            default: undefined,
        }
    },
    setup(props, { emit }) {
        const lengthExercise = ref<number | string>('');
        const textExercise = ref('');
        const zoneKeyboard = ref<string[]>(props.keyboardZones);
        const selectedZones = ref<string[]>(props.keyboardZones);

        const handleSelectedValues = (values: string[]) => {
            zoneKeyboard.value = values;
            console.log(`Появились изменения cew ${values}`);
        };

        const changeTextExercise = (value: string) => {
            textExercise.value = value;
        };

        const changeLengthExercise = (value: number) => {
            lengthExercise.value = value;
        };

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const saveChanges = async () => {
            try {
                const response = await axios.post('/api/task/create', {
                    content: textExercise.value,
                    difficulty_id: props.difficultyId // Используем переданный difficulty_id
                });
                console.log('Сохраненные значения:', response.data);
                closeModal();
            } catch (error) {
                console.error('Ошибка при сохранении:', error);
            }
        };

        const getAllowedCharacters = (zones: string[]) => {
            return getZoneNameFromSelectedOptions(zones).join('') + ' ';
        };

        return {
            CloseUrl,
            lengthExercise,
            textExercise,
            zoneKeyboard,
            selectedZones,
            handleSelectedValues,
            changeTextExercise,
            changeLengthExercise,
            closeModal,
            saveChanges,
            getAllowedCharacters,
        };
    },
});
</script>

<style scoped>
.title {
    font-size: 20px;
    margin-bottom: 10px;
    color: #012E4A;
}

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
