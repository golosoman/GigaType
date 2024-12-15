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
                inputPlaceholder="Введите минимальное количество символов:" :modelValue="minCountChar"
                @update:modelValue="changeMinCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <div v-if="minCountError" style="color: red;">{{ minCountError }}</div>

            <BaseInputWithLabel label="Максимальное количество символов"
                inputPlaceholder="Введите максимальное количество символов:" :modelValue="maxCountChar"
                input-type="number" @update:modelValue="changeMaxCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" />
            <div v-if="maxCountError" style="color: red;">{{ maxCountError }}</div>

            <BaseInputWithLabel label="Время нажатия на клавишу" inputPlaceholder="Введите время нажатия на клавишу:"
                :modelValue="timePressKey" @update:modelValue="changeTimePressKey"
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
import { getUidsFromSelectedOptions } from '@/component/Trainer';
import { ZoneToNameZone } from '@/types';
import { validateMaxCountChar, validateMinCountChar, validateTimePressKey, validateZones } from '@/utils';

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
        const minCountChar = ref<number>(20);
        const maxCountChar = ref<number>(80);
        const timePressKey = ref<number>(1.5);
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
            validateZones(selectedOptions.value, zoneError);
        };

        const changeMinCountChar = (value: string) => {
            minCountChar.value = Number(value);
            validateMinCountChar(minCountChar, minCountError);
        };

        const changeMaxCountChar = (value: string) => {
            maxCountChar.value = Number(value);
            validateMaxCountChar(maxCountChar, minCountChar, maxCountError);
        };

        const changeTimePressKey = (value: string) => {
            timePressKey.value = parseFloat(value);
            validateTimePressKey(timePressKey, timePressError);
        };


        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const save = async () => {
            validateZones(selectedOptions.value, zoneError);
            validateMinCountChar(minCountChar, minCountError);
            validateMaxCountChar(maxCountChar, minCountChar, maxCountError);
            validateTimePressKey(timePressKey, timePressError);

            if (zoneError.value || minCountError.value || maxCountError.value || timePressError.value) {
                emit('show-error', zoneError.value || minCountError.value || maxCountError.value || timePressError.value);
                // console.log(minCountError.value || maxCountError.value || timePressError.value || zoneError)
                return;
            }

            const uids = getUidsFromSelectedOptions(selectedOptions.value, extractedZones.value, ZoneToNameZone);
            const payload = {
                name: 0,
                min_length: minCountChar.value,
                max_length: maxCountChar.value,
                key_press_time: timePressKey.value,
                max_mistakes: Math.floor((minCountChar.value + maxCountChar.value) / 2 * 0.1),
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
                emit('show-success', "Уровень сложности успешно создан!");
                closeModal();
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                    if (error.response?.status === 418) {
                        console.error('Достигнуто максимальное количество уровней:', error.response.data);
                        emit('show-error', 'Достигнуто максимальное количество уровней.');
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

        return {
            minCountChar,
            maxCountChar,
            timePressKey,
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
