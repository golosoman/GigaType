<template>
    <div class="trainer-container">
        <div class="full-width">
            <div>Упражнение {{ level }}.{{ exercise }}</div>
            <div>Количество символов {{ textFromInput.length }}/{{ textToType.length }}</div>
            <div>Скорость: {{ speed }} симв/мин</div>
            <div>Ошибки: {{ errorsCount }}/{{ maxErrors }}</div>
            <div>Время: {{ elapsedTime }} сек</div>
            <div>Счет: {{ score }}</div>
        </div>
        <TrainingField :textToType="textToType" :customStyle="customStyleForTrainingField"
            :disabled="errorsCount >= maxErrors" ref="trainingField" v-model:inputText="textFromInput"
            v-model:textPreview="textPreview" v-model:inputControl="trackClicks" @completed="handleCompletion"
            @invalid-character="handleInvalidCharacter" @right-character="handleUpdateTextInput"
            @current-charrecter="handleThrowCurrentCharacter" />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onBeforeUnmount, onMounted } from 'vue';
import { TrainingField } from '.';

export default defineComponent({
    name: 'TypingTrainer',
    components: {
        TrainingField,
    },
    props: {
        level: {
            type: String,
            required: true,
        },
        exercise: {
            type: String,
            required: true,
        },
        maxErrors: {
            type: Number,
            required: true,
        },
        textToType: {
            type: String,
            required: true,
        },
        maxKeyPressInterval: {
            type: Number,
            default: 1500,
        },
        customStyleForTrainingField: {
            type: String,
            default: '',
        },
    },
    setup(props, { emit }) {
        // Данные статистики
        const speed = ref(0);
        const errorsCount = ref(0);
        const elapsedTime = ref(0);
        const score = ref(0);
        const lastKeyPressTime = ref(0);

        // Отслеживать нажатия
        const trackClicks = ref(false);
        const textFromInput = ref('');
        const textPreview = ref('Нажмите «SPACE»');
        const firstCharacter = ref('');

        // Флаг для отслеживания состояния таймера (возможно таймер или отслеживание кликов можно удалить)
        const timerRunning = ref(false);
        let timer: ReturnType<typeof setInterval>;
        let pressTimer: ReturnType<typeof setInterval>;

        const calculateScore = () => {
            const timeBonus = Math.max(0, 120 - elapsedTime.value);
            const errorPenalty = Math.pow(errorsCount.value + 5, 2);
            return Math.max(0, speed.value + timeBonus - errorPenalty);
        };

        const updateSpeed = () => {
            speed.value = Math.max(0, Math.round((textFromInput.value.length * 60) / elapsedTime.value));
            score.value = calculateScore();
        };

        const handleUpdateTextInput = (inputText: string) => {
            textFromInput.value = inputText;
            lastKeyPressTime.value = Date.now();
        };

        const handleThrowCurrentCharacter = (character: string) => {
            if (!timerRunning.value) {
                emit('current-charrecter', ' ')
                firstCharacter.value = character
            }
            else {
                emit('current-charrecter', character)
            }
        }

        const checkLastKeyPressTime = () => {
            const currentTime = Date.now();
            if (currentTime - lastKeyPressTime.value > props.maxKeyPressInterval) {
                console.log(`Превышено ожидание нажатия на клавишу! ${currentTime - lastKeyPressTime.value} против ${props.maxKeyPressInterval}`);
                resetStatistics();
            }
            lastKeyPressTime.value = currentTime;
        };

        const handleCompletion = (inputText: string) => {
            console.log('Завершено:', inputText);
            clearInterval(timer);
            timerRunning.value = false; // Остановить таймер
            // Эмитируем успешное завершение
            emit('success-completion', [
                props.level,
                props.exercise,
                speed.value,
                errorsCount.value,
                elapsedTime.value,
                score.value,
                textFromInput.value.length
            ]);
        };

        const handleInvalidCharacter = (invalidChar: string) => {
            lastKeyPressTime.value = Date.now();
            if (errorsCount.value < props.maxErrors) {
                errorsCount.value += 1;
                console.log(`Неверный символ: ${invalidChar}`);
            }
            if (errorsCount.value >= props.maxErrors) {
                console.log('Тренировка завершена из-за превышения максимального количества ошибок.');
                resetStatistics();
                // Эмитируем завершение с ошибками
                emit('error-completion', [
                    props.level,
                    props.exercise,
                    speed.value,
                    errorsCount.value,
                    elapsedTime.value,
                    score.value,
                    textFromInput.value.length
                ]);
            }
        };

        const resetStatistics = () => {
            clearInterval(timer);
            clearInterval(pressTimer);
            score.value = 0;
            trackClicks.value = false;
            timerRunning.value = false; // Остановить таймер
        };

        const startTimer = () => {
            if (!timerRunning.value) {
                emit('current-charrecter', firstCharacter.value);
                firstCharacter.value = '';
                textPreview.value = "";
                textFromInput.value = "";
                trackClicks.value = true;
                lastKeyPressTime.value = Date.now();
                timerRunning.value = true; // Установить флаг, что таймер запущен
                timer = setInterval(() => {
                    elapsedTime.value += 1;
                    updateSpeed();
                }, 1000);
                pressTimer = setInterval(() => {
                    if (timerRunning.value) {
                        checkLastKeyPressTime()
                    }
                }, props.maxKeyPressInterval);
            }
        };

        const handleKeyClick = (event: KeyboardEvent) => {
            if (event.key === " ") {
                startTimer();
                window.removeEventListener('keydown', handleKeyClick);
            }
        };

        onMounted(() => {
            window.addEventListener('keydown', handleKeyClick);
        });

        onBeforeUnmount(() => {
            clearInterval(timer);
            window.removeEventListener('keydown', handleKeyClick);
        });

        return {
            speed,
            errorsCount,
            elapsedTime,
            score,
            trackClicks,
            textFromInput,
            timerRunning,
            textPreview,
            handleThrowCurrentCharacter,
            handleCompletion,
            handleInvalidCharacter,
            handleUpdateTextInput,
            startTimer,
        };
    },
});
</script>

<style scoped>
.full-width {
    width: 100%;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    margin-bottom: 10px;
    color: #012e4a;
    font-family: "Alegreya Sans SC";
    font-size: 30px;
}

.trainer-container {
    display: flex;
    flex-direction: column;
    width: fit-content;
}
</style>
