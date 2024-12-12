<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Создание уровня сложности
            </div>
            <KeyboardWithCheckbox @update:selectedValues="handleSelectedValues" :keyboard-zones="selectedOptions">
            </KeyboardWithCheckbox>
            <div v-if="zoneError" style="color: red;">{{ zoneError }}</div>
            <BaseInputWithLabel label="Минимальное количество символов" input-type="number"
                inputPlaceholder="Введите минимальное количество символов:" :modelValue="min_count_char"
                @update:modelValue="changeMinCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <div v-if="minCountError" style="color: red;">{{ minCountError }}</div>

            <BaseInputWithLabel label="Максимальное количество символов"
                inputPlaceholder="Введите максимальное количество символов:" :modelValue="max_count_char"
                input-type="number" @update:modelValue="changeMaxCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" />
            <div v-if="maxCountError" style="color: red;">{{ maxCountError }}</div>

            <BaseInputWithLabel label="Время нажатия на клавишу" inputPlaceholder="Введите время нажатия на клавишу:"
                :modelValue="time_press_key" @update:modelValue="changeTimePressKey"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" input-type="number" />
            <div v-if="timePressError" style="color: red;">{{ timePressError }}</div>

            <BaseButton @click="save"
                customStyle="width: 150px; height: 30px; border-radius: 15px; margin-top: 41px; font-size: 20px; color: #012E4A;">
                Сохранить
            </BaseButton>
            <ButtonWithImage class="close-button" @click="closeModal" :imageSrc="CloseUrl"
                customStyle="background-color: #D9D9D9;" customStyleForImage="width: 30px; height: 30px;">
            </ButtonWithImage>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { KeyboardWithCheckbox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import axios from 'axios';
import CloseUrl from '@/assets/Close.png';
import { getUidsFromSelectedOptions } from '@/component/Trainer/modalWindow';

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
        const min_count_char = ref<number>(20);
        const max_count_char = ref<number>(80);
        const time_press_key = ref<number>(1.5);
        const selectedOptions = ref<string[]>([]);
        const extractedZones = ref<{ keys: string, uid: string }[]>([]);

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
            selectedOptions.value = values;
            validateZones();
        };

        const changeMinCountChar = (value: string) => {
            min_count_char.value = Number(value);
            validateMinCountChar();
        };

        const changeMaxCountChar = (value: string) => {
            max_count_char.value = Number(value);
            validateMaxCountChar();
        };

        const changeTimePressKey = (value: string) => {
            time_press_key.value = parseFloat(value);
            validateTimePressKey();
        };

        const validateZones = () => {
            console.log(selectedOptions.value.length)
            if (selectedOptions.value.length === 0) {
                zoneError.value = "Нужно выбрать хотя бы одну зону!"
            } else {
                zoneError.value = '';
            }
        }

        const validateMinCountChar = () => {
            if (min_count_char.value === null || min_count_char.value === undefined || String(min_count_char.value) === '') {
                minCountError.value = 'Минимальное количество символов не должно быть пустым.';
            } else if (min_count_char.value < 20 || min_count_char.value > 80) {
                minCountError.value = 'Минимальное количество символов должно быть от 20 до 80.';
            } else {
                minCountError.value = '';
            }
        };

        const validateMaxCountChar = () => {
            if (max_count_char.value === null || max_count_char.value === undefined || String(min_count_char.value) === '') {
                maxCountError.value = 'Максимальное количество символов не должно быть пустым.';
            } else if (max_count_char.value < 20 || max_count_char.value > 80) {
                maxCountError.value = 'Максимальное количество символов должно быть от 20 до 80.';
            } else if (max_count_char.value <= min_count_char.value + 9) {
                maxCountError.value = 'Максимальное количество символов должно быть больше минимального на 10.';
            } else {
                maxCountError.value = '';
            }
        };

        const validateTimePressKey = () => {
            if (time_press_key.value === null || time_press_key.value === undefined || String(time_press_key.value) === '') {
                timePressError.value = 'Время нажатия на клавишу не должно быть пустым.';
            } else if (time_press_key.value < 0.5 || time_press_key.value > 1.5) {
                timePressError.value = 'Время нажатия на клавишу должно быть от 0.5 до 1.5.';
            } else {
                timePressError.value = '';
            }
        };

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const save = async () => {
            validateMinCountChar();
            validateMaxCountChar();
            validateTimePressKey();
            validateZones();

            if (minCountError.value || maxCountError.value || timePressError.value || zoneError.value) {
                emit('show-error', minCountError.value || maxCountError.value || timePressError.value || zoneError.value);
                // console.log(minCountError.value || maxCountError.value || timePressError.value || zoneError)
                return;
            }

            const uids = getUidsFromSelectedOptions(selectedOptions.value, extractedZones.value, ZoneToNameZone);
            const payload = {
                name: 0,
                min_length: min_count_char.value,
                max_length: max_count_char.value,
                key_press_time: time_press_key.value,
                max_mistakes: Math.floor((min_count_char.value + max_count_char.value) / 2 * 0.1),
                zones: uids
            };

            try {
                const response = await axios.post('/api/difficulty/create', payload, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    withCredentials: true,
                });
                console.log('Ответ от сервера:', response);
                emit('show-success', minCountError.value || maxCountError.value || timePressError.value || zoneError.value);
                closeModal();
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                } else {
                    console.error('Неизвестная ошибка:', error);
                }
            }
        };

        return {
            min_count_char,
            max_count_char,
            time_press_key,
            selectedOptions,
            CloseUrl,
            changeTimePressKey,
            changeMaxCountChar,
            changeMinCountChar,
            closeModal,
            handleSelectedValues,
            minCountError,
            maxCountError,
            timePressError,
            zoneError,
            save,
            extractedZones
        };
    },
});
</script>

<style scoped>
/* Hide the spin buttons in WebKit browsers */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

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
