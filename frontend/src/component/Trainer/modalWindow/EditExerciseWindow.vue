<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Изменение упражнения
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
            <BaseInputTextArea :allowedCharacters="getAllowedCharacters(keyboardZones)" :modelValue="textsExercise"
                @update:modelValue="changeTextExercise" />
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
import { defineComponent, ref, watch, onMounted } from 'vue';
import { KeyboardWithBlockCheckBox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage, BaseInput, BaseInputTextArea } from '@/component/UI';
import CloseUrl from '@/assets/Close.png';
import axios from 'axios';
import { getZoneNameFromSelectedOptions, getUidsFromSelectedOptions } from '@/component/Trainer/modalWindow';

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
        keyboardZonesForTask: {
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
        },
        taskId: {
            type: String,
            required: false,
            default: undefined,
        },
        textExercise: {
            type: String,
            required: true,
        }
    },
    setup(props, { emit }) {
        const zoneKeyboard = ref(props.keyboardZones);
        const lengthExercise = ref<number | string>('');
        const textsExercise = ref(props.textExercise);
        const lengthError = ref('');
        const textError = ref('');
        const zoneError = ref('');

        watch(() => props.keyboardZones, (newZones) => {
            zoneKeyboard.value = newZones;
            console.log(`Зоны изменились! ${newZones}`);
        });

        watch(() => props.textExercise, (newValue) => {
            textsExercise.value = newValue;
            console.log('textsExercise изменился на:', newValue);
        });

        const handleSelectedValues = (values: string[]) => {
            zoneKeyboard.value = values;
            validateSelectedZones();
            console.log(`Появились изменения cew ${zoneKeyboard.value}`);
        };

        const changeTextExercise = (value: string) => {
            textsExercise.value = value;
            validateTextExercise();
        };

        const changeLengthExercise = (value: number) => {
            lengthExercise.value = value;
            validateLengthExercise();
        };

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        type ZoneKey =
            | "Зона 1 (ФЫВАОЛДЖ)"
            | "Зона 2 (ПР)"
            | "Зона 3 (КЕНГ)"
            | "Зона 4 (МИТЬ)"
            | "Зона 5 (УСШБ)"
            | "Зона 6 (ЦЧЩЮ)"
            | "Зона 7 (ЁЙЯЗХЪЭ.,)"
            | "Зона 8 (1234567890)"
            | "Зона 9 (символы)"
            | "Зона Пробела";

        const ZoneToNameZone: Record<ZoneKey, string> = {
            "Зона 1 (ФЫВАОЛДЖ)": "фываолдж",
            "Зона 2 (ПР)": "пр",
            "Зона 3 (КЕНГ)": "кенг",
            "Зона 4 (МИТЬ)": "мить",
            "Зона 5 (УСШБ)": "усшб",
            "Зона 6 (ЦЧЩЮ)": "цчщю",
            "Зона 7 (ЁЙЯЗХЪЭ.,)": "ёйязхъэ.,",
            "Зона 8 (1234567890)": "1234567890",
            "Зона 9 (символы)": '!"№;%:?*()_-+=',
            "Зона Пробела": " ",
        };

        const saveChanges = async () => {
            validateTextExercise();
            if (textError.value) {
                emit('show-error', textError.value);
                return;
            }

            const requestBody = {
                uid: props.taskId,
                difficulty_id: props.difficultyId,
                content: textsExercise.value,
                zones: getUidsFromSelectedOptions(zoneKeyboard.value, extractedZones.value, ZoneToNameZone)
            };
            console.log(requestBody)
            try {

                const response = await axios.patch('/api/task/update', requestBody, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                console.log('Упражнение обновлено успешно:', response.data);
                emit('show-success', "Упражнение успешно обновлено!");
                closeModal();
            } catch (error) {
                console.error('Ошибка при обновлении упражнения:', error);
                emit('show-error', `Ошибка при обновлении упражнения: ${error}`);
            }
        };

        const extractedZones = ref<{ keys: string, uid: string }[]>([]);

        const fetchZones = async () => {
            try {
                const response = await axios.get('/api/zone/get', { withCredentials: true });
                console.log('Зоны:', response.data);
                extractedZones.value = response.data;
            } catch (error) {
                console.error('Ошибка при получении зон:', error);
            }
        };

        onMounted(() => {
            fetchZones();
        });

        const validateSelectedZones = () => {
            if (zoneKeyboard.value.length === 0) {
                zoneError.value = "Нужно выбрать хотя бы одну зону!";
            } else {
                zoneError.value = '';
            }
        };

        const validateLengthExercise = () => {
            const length = Number(lengthExercise.value);
            if (length < props.minCount || length > props.maxCount) {
                lengthError.value = `Количество символов должно быть от ${props.minCount} до ${props.maxCount}.`;
            } else {
                lengthError.value = '';
            }
        };

        const validateTextExercise = () => {
            const length = textsExercise.value.length; // Получаем длину текста
            if (length < props.minCount) {
                textError.value = `Текст упражнения должен содержать минимум ${props.minCount} символов.`;
            } else if (length > props.maxCount) {
                textError.value = `Текст упражнения не должен превышать ${props.maxCount} символов.`;
            } else {
                textError.value = ''; // Если длина текста в допустимых пределах, очищаем ошибку
            }
        };

        const generateExercise = async () => {
            validateSelectedZones();
            validateLengthExercise();
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

                textsExercise.value = response.data.content;
                console.log('Сгенерированное упражнение:', response.data.content);
                emit('show-success', "Упражнение успешно сгенерировано!");
            } catch (error) {
                console.error('Ошибка при генерации упражнения:', error);
                emit('show-error', `Ошибка при генерации упражнения: ${error}`);
            }
        };

        const getAllowedCharacters = (zones: string[]) => {
            return getZoneNameFromSelectedOptions(zones).join('') + ' ';
        };

        return {
            textsExercise,
            CloseUrl,
            zoneKeyboard,
            lengthExercise,
            handleSelectedValues,
            generateExercise,
            getAllowedCharacters,
            changeTextExercise,
            changeLengthExercise,
            closeModal,
            saveChanges,
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
