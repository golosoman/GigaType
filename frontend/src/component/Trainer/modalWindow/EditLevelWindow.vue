<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Изменение уровня сложности
            </div>
            <KeyboardWithCheckbox @update:selectedValues="handleSelectedValues" :keyboardZones="zoneKeyboard" />
            <BaseInputWithLabel label="Минимальное количество символов"
                inputPlaceholder="Введите минимальное количество символов:" :modelValue="minCountChar"
                @update:modelValue="changeMinCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <BaseInputWithLabel label="Максимальное количество символов"
                inputPlaceholder="Введите максимальное количество символов:" :modelValue="maxCountChar"
                @update:modelValue="changeMaxCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <BaseInputWithLabel label="Время нажатия на клавишу" inputPlaceholder="Введите время нажатия на клавишу:"
                :modelValue="timePressKey" @update:modelValue="changeTimePressKey"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <BaseButton
                customStyle="width: 150px; height: 30px; border-radius: 15px; margin-top: 41px; font-size: 20px; color: #012E4A;"
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
import { defineComponent, ref, onMounted } from 'vue';
import { KeyboardWithCheckbox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import CloseUrl from '@/assets/Close.png';
import axios from 'axios';
import { transformZones, getUidsFromSelectedOptions } from '@/component/Trainer/modalWindow'

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
        // Пример использования
        const zoneKeyboard = ref(transformZones(props.keyboardZones)); // Преобразуем зоны
        console.log(`Вот прилетели зоны: ${zoneKeyboard.value}`);
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

        const handleSelectedValues = (values: string[]) => {
            zoneKeyboard.value = values;
            console.log(`Появились изменения ${values}`);
        };
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

        const saveChanges = async () => {

            const payload = {
                uid: props.difficultyId, // Используем uid из пропсов
                min_length: minCountChar.value,
                max_length: maxCountChar.value,
                key_press_time: timePressKey.value,
                max_mistakes: maxErrors.value, // Убедитесь, что maxErrors определен в вашем компоненте
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
                // console.log(payload)
                // Можно добавить логику для уведомления пользователя об успешном обновлении уровня сложности
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.error('Ошибка при отправке запроса:', error.response?.data || error.message);
                } else {
                    console.error('Неизвестная ошибка:', error);
                }
            }

            closeModal();
        };

        return {
            minCountChar,
            maxCountChar,
            timePressKey,
            CloseUrl,
            zoneKeyboard,
            handleSelectedValues,
            transformZones,
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
