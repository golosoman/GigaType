<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div>
                Создание уровня сложности
            </div>
            <KeyboardWithBlockCheckBox :keyboardZones="keyboardZones" />
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
            <BaseInputTextArea :allowedCharacters="getAllowedCharacters(keyboardZones)" :modelValue="textsExercise"
                @update:modelValue="changeTextExercise" />
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
import { defineComponent, ref, watch } from 'vue';
import { KeyboardWithBlockCheckBox } from '../keyboard';
import { BaseInputWithLabel, BaseButton, ButtonWithImage, BaseInput, BaseInputTextArea } from '@/component/UI';
import CloseUrl from '@/assets/Close.png';
import { getZoneNameFromSelectedOptions } from '@/component/Trainer/modalWindow';

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
        difficultyId: {
            type: String,
            required: false, // или уберите это, если хотите сделать его необязательным
            default: undefined,
        },
        taskId: {
            type: String,
            required: false, // или уберите это, если хотите сделать его необязательным
            default: undefined,
        },
        textExercise: {
            type: String,
            required: true,
        }
    },
    setup(props, { emit }) {
        const zoneKeyboard = ref(props.keyboardZones);
        const lengthExercise = ref<number | string>('')

        const textsExercise = ref(props.textExercise); // Создаем реактивную переменную

        // Подписываемся на изменения props.textExercise
        watch(() => props.textExercise, (newValue) => {
            textsExercise.value = newValue; // Обновляем textsExercise при изменении пропса
        });

        // Подписываемся на изменения textsExercise
        watch(textsExercise, (newValue) => {
            console.log('textsExercise изменился на:', newValue);
            // Здесь вы можете выполнять дополнительные действия при изменении textsExercise
        });

        const changeTextExercise = (value: string) => {
            textsExercise.value = value; // Обновляем значение textsExercise
        };

        const changeLengthExercise = (value: number) => {
            lengthExercise.value = value
        }

        const closeModal = () => {
            emit('update:isVisible', false);
        };

        const saveChanges = async () => {
            // Создаем тело запроса
            const requestBody = {
                uid: props.taskId, // uid задания
                difficulty_id: props.difficultyId, // uid сложности
                content: textsExercise.value // введенный текст
            };

            try {
                const response = await fetch('/api/task/update', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody),
                });

                if (!response.ok) {
                    throw new Error('Ошибка при обновлении упражнения');
                }

                const result = await response.json();
                console.log('Упражнение обновлено успешно:', result);
                closeModal(); // Закрываем модальное окно после успешного обновления

            } catch (error) {
                console.error('Ошибка при обновлении упражнения:', error);
                // Здесь вы можете отобразить сообщение об ошибке пользователю, если это необходимо
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
            getAllowedCharacters,
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