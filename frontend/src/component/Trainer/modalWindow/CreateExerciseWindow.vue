<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Создание упражнения
            </div>
            <KeyboardWithBlockCheckBox @update:selectedOptions="handleSelectedValues" :keyboardZones="keyboardZones" />
            <div v-if="zoneError" style="color: red;">{{ zoneError }}</div>
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
                    <div v-if="lengthError" style="color: red;">{{ lengthError }}</div>
                    <BaseButton @click="generateExercise"
                        customStyle="width: 250px; height: 30px; font-size: 20px; border-radius: 15px; margin-top: 10px; color: #012E4A;">
                        Генерация упражнения
                    </BaseButton>
                </div>
            </div>
            <BaseInputTextArea v-model="textExercise" @update:modelValue="changeTextExercise"
                inputPlaceholder="Введите текст упражнения:" :allowedCharacters="getAllowedCharacters(keyboardZones)" />
            <div v-if="textError" style="color: red;">{{ textError }}</div>
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
import { defineComponent, ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { KeyboardWithBlockCheckBox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage, BaseInput, BaseInputTextArea } from '@/component/UI';
import { getZoneNameFromSelectedOptions, getUidsFromSelectedOptions } from '@/component/Trainer';
import CloseUrl from '@/assets/Close.png';
import { ZoneToNameZone } from '@/types';
import { validateLengthExercise, validateTextExercise, validateZones } from '@/utils';

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
            required: false,
            default: undefined,
        }
    },
    setup(props, { emit }) {
        const lengthExercise = ref<number | string>('');
        const textExercise = ref('');
        const zoneKeyboard = ref<string[]>(props.keyboardZones);
        const lengthError = ref('');
        const textError = ref('');
        const zoneError = ref('');

        watch(() => props.keyboardZones, (newZones) => {
            zoneKeyboard.value = newZones;
            console.log(`Зоны изменились! ${newZones}`);
        });

        const handleSelectedValues = (values: string[]) => {
            zoneKeyboard.value = values;
            validateZones(zoneKeyboard.value, zoneError);
            console.log(`Появились изменения cew ${zoneKeyboard.value}`);
        };

        const changeTextExercise = (value: string) => {
            textExercise.value = value;
            validateTextExercise(textExercise, props.minCount, props.maxCount, textError);
        };

        const changeLengthExercise = (value: number) => {
            lengthExercise.value = value;
            validateLengthExercise(lengthExercise, props.minCount, props.maxCount, lengthError);
        };

        const closeModal = () => {
            textExercise.value = '';
            emit('update:isVisible', false);
        };

        const extractedZones = ref<{ keys: string, uid: string }[]>([]);

        const fetchZones = async () => {
            try {
                const response = await axios.get('/api/zone/get', { withCredentials: true });
                console.log('Зоны:', response.data);
                extractedZones.value = response.data; // Сохраняем данные зон
            } catch (error) {
                console.error('Ошибка при получении зон:', error);
            }
        };

        onMounted(() => {
            fetchZones();
        });

        const saveChanges = async () => {
            validateTextExercise(textExercise, props.minCount, props.maxCount, textError);
            if (textError.value) {
                emit('show-error', textError.value);
                return;
            }

            try {
                const uids = getUidsFromSelectedOptions(zoneKeyboard.value, extractedZones.value, ZoneToNameZone);
                const response = await axios.post('/api/task/create', {
                    content: textExercise.value,
                    difficulty_id: props.difficultyId, // Используем переданный difficulty_id
                    zones: uids
                });
                console.log('Сохраненные значения:', response.data);
                emit('show-success', "Упражнение успешно создано!");
                closeModal();
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                    if (error.response?.status === 418) {
                        console.error('Достигнуто максимальное количество упражнений:', error.response.data);
                        emit('show-error', 'Достигнуто максимальное количество упражнений.');
                    } else {
                        console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                        emit('show-error', `Ошибка при отправке запроса: ${error.message}`);
                    }
                } else {
                    console.error('Неизвестная ошибка:', error);
                    emit('show-error', `Неизвестная ошибка: ${error}`)
                }
            }
        };

        const generateExercise = async () => {
            validateZones(zoneKeyboard.value, zoneError);
            validateLengthExercise(lengthExercise, props.minCount, props.maxCount, lengthError);
            if (lengthError.value || zoneError.value) {
                emit('show-error', lengthError.value || zoneError.value);
                return;
            }

            try {
                const uids = getUidsFromSelectedOptions(zoneKeyboard.value, extractedZones.value, ZoneToNameZone);
                const response = await axios.post('/api/content/generate', {
                    uids: uids,
                    length: lengthExercise.value
                });

                textExercise.value = response.data.content; // Устанавливаем текст упражнения
                console.log('Сгенерированное упражнение:', response.data.content);
                emit('show-success', "Упражнение успешно сгенерировано!");
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                    if (error.response?.status === 418) {
                        console.error('Достигнуто максимальное количество упражнений:', error.response.data);
                        emit('show-error', 'Достигнуто максимальное количество упражнений.');
                    } else {
                        console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                        emit('show-error', `Ошибка при отправке запроса: ${error.message}`);
                    }
                } else {
                    console.error('Неизвестная ошибка:', error);
                    emit('show-error', `Неизвестная ошибка: ${error}`)
                }
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
            handleSelectedValues,
            changeTextExercise,
            changeLengthExercise,
            closeModal,
            saveChanges,
            generateExercise,
            getAllowedCharacters,
            lengthError,
            textError,
            zoneError,
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
