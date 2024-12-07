<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="title">
                Создание уровня сложности
            </div>
            <KeyboardWithCheckbox @update:selectedValues="handleSelectedValues">
            </KeyboardWithCheckbox>
            <BaseInputWithLabel label="Минимальное количество символов"
                inputPlaceholder="Введите минимальное количество символов:" :modelValue="min_count_char"
                @update:modelValue="changeMinCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px;" />
            <BaseInputWithLabel label="Максимальное количество символов"
                inputPlaceholder="Введите максимальное количество символов:" :modelValue="max_count_char"
                input-type="number" @update:modelValue="changeMaxCountChar"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" />
            <BaseInputWithLabel label="Время нажатия на клавишу" inputPlaceholder="Введите время нажатия на клавишу:"
                :modelValue="time_press_key" @update:modelValue="changeTimePressKey"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" input-type="number" />
            <BaseInputWithLabel label="Максимальное количество ошибок"
                inputPlaceholder="Максимальное количество ошибок:" :modelValue="maxErrors"
                customStyleForInput="width: 500px; height: 30px; font-size: 20px; background-color: #B7BBBC;"
                customStyleForLabel="font-size: 20px; margin-top:10px;" input-type="number" />
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
import { defineComponent, ref, computed, onMounted } from 'vue';
import { KeyboardWithCheckbox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage } from '@/component/UI';
import axios from 'axios';
import CloseUrl from '@/assets/Close.png';

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
        const min_count_char = ref<number>(20);
        const max_count_char = ref<number>(80);
        const time_press_key = ref<number>(1.5);
        const selectedOptions = ref<string[]>([]);
        const extractedZones = ref<string[]>([]);

        // Новый метод для получения зон с сервера
        const fetchZones = async () => {
            try {
                const response = await axios.get('/api/zone/get', { withCredentials: true });
                console.log('Зоны:', response.data);
                // Извлекаем uid из полученных данных
                extractedZones.value = response.data.map((zone: { uid: string }) => zone.uid);
            } catch (error) {
                console.error('Ошибка при получении зон:', error);
            }
        };

        // Вызов fetchZones при монтировании компонента
        onMounted(() => {
            fetchZones();
        });

        const handleSelectedValues = (values: string[]) => {
            selectedOptions.value = values;
            console.log(`Появились изменения ${values}`);
        };

        const changeMinCountChar = (value: string) => {
            min_count_char.value = Number(value);
        };

        const changeMaxCountChar = (value: string) => {
            max_count_char.value = Number(value);
        };

        const changeTimePressKey = (value: string) => {
            time_press_key.value = parseFloat(value);
        };

        const maxErrors = computed(() => {
            if (min_count_char.value && max_count_char.value) {
                const average = (min_count_char.value + max_count_char.value) / 2;
                return Math.floor(average * 0.1);
            }
            return 0;
        });

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const save = async () => {
            const payload = {
                name: 0, // Название будет сгенерировано на сервере
                min_length: min_count_char.value,
                max_length: max_count_char.value,
                key_press_time: time_press_key.value,
                max_mistakes: maxErrors.value,
                zones: extractedZones.value // Используем извлеченные uid
            };

            try {
                const response = await axios.post('/api/difficulty/create', payload, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    withCredentials: true,
                });
                console.log('Ответ от сервера:', response.data);
                // Можно добавить логику для уведомления пользователя об успешном создании уровня сложности
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
            maxErrors,
            save,
            extractedZones // Возвращаем извлеченные зоны, если нужно использовать их в шаблоне
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
