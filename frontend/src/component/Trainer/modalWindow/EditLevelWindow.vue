<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Изменение уровня сложности
            </div>
            <KeyboardWithCheckbox @update:selectedValues="handleSelectedValues" :keyboard-zones="zoneKeyboard" />
            <div v-if="zoneError" style="color: red;">{{ zoneError }}</div>
            <BaseInputWithLabel label="Минимальное количество символов"
                inputPlaceholder="Введите минимальное количество символов:" :modelValue="minCountChar"
                @update:modelValue="changeMinCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <div v-if="minCountError" style="color: red;">{{ minCountError }}</div>

            <BaseInputWithLabel label="Максимальное количество символов"
                inputPlaceholder="Введите максимальное количество символов:" :modelValue="maxCountChar"
                @update:modelValue="changeMaxCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <div v-if="maxCountError" style="color: red;">{{ maxCountError }}</div>

            <BaseInputWithLabel label="Время нажатия на клавишу" inputPlaceholder="Введите время нажатия на клавишу:"
                :modelValue="timePressKey" @update:modelValue="changeTimePressKey"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <div v-if="timePressError" style="color: red;">{{ timePressError }}</div>

            <BaseButton
                customStyle="width: 150px; height: 30px; border-radius: 15px; margin-top: 41px; font-size: 20px; color: #012E4A;"
                @click="saveChanges">
                Сохранить
            </BaseButton>
            <ButtonWithImage class="close-button" @click="closeModal" :imageSrc="CloseUrl"
                customStyle="background-color: #D9D9D9;" customStyleForImage="width: 30px;">
            </ButtonWithImage>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { KeyboardWithCheckbox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import CloseUrl from '@/assets/Close.png';
import axios from 'axios';
import { transformZones, getUidsFromSelectedOptions } from '@/component/Trainer/modalWindow';

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
            type: Array as () => { keys: string; uid: string }[],
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
        },
        maxErrors: {
            type: Number,
            required: true,
        },
        difficultyId: {
            type: String,
            required: false,
            default: null,
        },
        taskId: {
            type: String,
            required: true,
        }
    },
    setup(props, { emit }) {
        const ZoneToNameZone = {
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

        const minCountChar = ref(props.minCount);
        const maxCountChar = ref(props.maxCount);
        const timePressKey = ref(props.timePressKey);
        const maxErrors = ref(props.maxErrors);
        const zoneKeyboard = ref(transformZones(props.keyboardZones));
        const extractedZones = ref<{ keys: string, uid: string }[]>([]);

        // Валидационные ошибки
        const minCountError = ref('');
        const maxCountError = ref('');
        const timePressError = ref('');
        const zoneError = ref('');

        const fetchZones = async () => {
            try {
                const response = await axios.get('/api/zone/get', { withCredentials: true });
                extractedZones.value = response.data;
            } catch (error) {
                console.error('Ошибка при получении зон:', error);
            }
        };

        onMounted(() => {
            fetchZones();
        });

        const handleSelectedValues = (values: string[]) => {
            zoneKeyboard.value = values;
            validateZones();
        };

        const changeMinCountChar = (value: number) => {
            minCountChar.value = value;
            validateMinCountChar();
        };

        const changeMaxCountChar = (value: number) => {
            maxCountChar.value = value;
            validateMaxCountChar();
        };

        const changeTimePressKey = (value: number) => {
            timePressKey.value = value;
            validateTimePressKey();
        };

        const validateZones = () => {
            if (zoneKeyboard.value.length === 0) {
                zoneError.value = "Нужно выбрать хотя бы одну зону!";
            } else {
                zoneError.value = '';
            }
        };

        const validateMinCountChar = () => {
            if (minCountChar.value < 20 || minCountChar.value > 80) {
                minCountError.value = 'Минимальное количество символов должно быть от 20 до 80.';
            } else {
                minCountError.value = '';
            }
        };

        const validateMaxCountChar = () => {
            if (maxCountChar.value < 20 || maxCountChar.value > 80) {
                maxCountError.value = 'Максимальное количество символов должно быть от 20 до 80.';
            } else if (maxCountChar.value <= minCountChar.value + 9) {
                maxCountError.value = 'Максимальное количество символов должно быть больше минимального на 10.';
            } else {
                maxCountError.value = '';
            }
        };

        const validateTimePressKey = () => {
            if (timePressKey.value < 0.5 || timePressKey.value > 1.5) {
                timePressError.value = 'Время нажатия на клавишу должно быть от 0.5 до 1.5.';
            } else {
                timePressError.value = '';
            }
        };

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const saveChanges = async () => {
            validateMinCountChar();
            validateMaxCountChar();
            validateTimePressKey();
            validateZones();

            if (minCountError.value || maxCountError.value || timePressError.value || zoneError.value) {
                emit('show-error', minCountError.value || maxCountError.value || timePressError.value || zoneError.value);
                return;
            }

            const payload = {
                uid: props.difficultyId,
                min_length: minCountChar.value,
                max_length: maxCountChar.value,
                key_press_time: timePressKey.value,
                max_mistakes: maxErrors.value,
                zones: getUidsFromSelectedOptions(zoneKeyboard.value, extractedZones.value, ZoneToNameZone)
            };

            try {
                const response = await axios.patch('/api/difficulty/update', payload, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    withCredentials: true,
                });
                console.log('Ответ от сервера:', response.data);
                emit('show-success', 'Уровень сложности успешно обновлен!');
                closeModal();
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                    emit('show-error', `Ошибка при отправке запроса: ${error.response?.data || error.message}`)
                } else {
                    console.error('Неизвестная ошибка:', error);
                    emit('show-error', `Неизвестная ошибка: ${error}`)
                }
            }
        };

        return {
            minCountChar,
            maxCountChar,
            timePressKey,
            CloseUrl,
            zoneKeyboard,
            handleSelectedValues,
            changeMinCountChar,
            changeMaxCountChar,
            changeTimePressKey,
            closeModal,
            saveChanges,
            minCountError,
            maxCountError,
            timePressError,
            zoneError
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