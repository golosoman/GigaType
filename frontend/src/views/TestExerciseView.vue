<script setup lang="ts">
import { Keyboard, TypingTrainer, NavigationBarForTrainee, FinishExerciseWindow } from '@/component/Trainer';
import { BaseCheckbox } from '@/component/UI';
import { ref } from 'vue';

interface CompletionData {
    level: string;
    exercise: string;
    speed: number;
    errorsCount: number;
    elapsedTime: number;
    score: number;
    numbersCount: number;
}

const isModalVisible = ref(false);
const resultData = ref<CompletionData>({
    level: "",
    exercise: "Быстрая коричневая лиса прыгает через ленивую собаку на зеленом лугу.",
    speed: 0,
    errorsCount: 0,
    elapsedTime: 0,
    score: 0,
    numbersCount: 0
});

const exerciseData = ref<CompletionData>({
    level: "",
    exercise: "На горизонте в 5 часов вечера появилось 3 ярких солнца, освещая 7 волшебных островов, где 12 мифических существ охраняли древние тайны природы.",
    speed: 0,
    errorsCount: 5, // Максимальное количество ошибок для начального уровня
    elapsedTime: 0,
    score: 0,
    numbersCount: 0
});

const showKeyboard = ref(false);
const currentCharacter = ref(' ');
const textToType = ref("На горизонте в 5 часов вечера появилось 3 ярких солнца, освещая 7 волшебных островов, где 12 мифических существ охраняли древние тайны природы."); // Статический текст

const calculateScore = (speed: number, errorsCount: number, elapsedTime: number, totalLength: number): number => {
    // Базовая скорость (например, 100 - это идеальная скорость)
    const baseSpeed = 100;

    // Учитываем ошибки: каждая ошибка уменьшает очки
    const errorPenalty = errorsCount * 5; // за каждую ошибку -5 очков

    // Учитываем время: чем дольше, тем меньше очков
    const timePenalty = Math.max(0, elapsedTime - 60) * 2; // за каждую минуту свыше 1 минуты -2 очка

    // Процент завершенного задания
    const completionRate = (totalLength > 0) ? (speed / totalLength) : 0;

    // Базовый расчет очков
    let score = speed - errorPenalty - timePenalty;

    // Учитываем процент завершения задания
    if (completionRate < 0.5) {
        score *= 0.5; // Если менее 50% текста введено, уменьшаем очки вдвое
    }

    // Убедимся, что очки не отрицательные
    return Math.max(0, score);
};

const determineLevel = (speed: number, errorsCount: number, elapsedTime: number, totalLength: number): string => {
    const adjustedSpeed = speed - (errorsCount * 2) - (elapsedTime / 60);
    const completionRate = (totalLength > 0) ? (speed / totalLength) : 0;

    const score = calculateScore(speed, errorsCount, elapsedTime, totalLength);
    if (completionRate < 0.7) {
        return "Не завершено";
    } else if (score < 280) {
        return "Начальный";
    } else if (score >= 280 && score < 300) {
        return "Средний";
    } else if (score >= 300) {
        return "Продвинутый";
    }
    return "Неопределенный уровень";
};

const handleSuccessCompletion = (data: any[]) => {
    const [level, exercise, speed, errorsCount, elapsedTime, score, numbersCount] = data;
    resultData.value = {
        level: determineLevel(speed, errorsCount, elapsedTime, numbersCount),
        exercise: exercise,
        speed: speed,
        errorsCount: errorsCount,
        elapsedTime: elapsedTime,
        score: score,
        numbersCount: numbersCount
    };
    isModalVisible.value = true;
};

const handleErrorCompletion = (data: any[]) => {
    const [level, exercise, speed, errorsCount, elapsedTime, score, numbersCount] = data;
    resultData.value = {
        level: determineLevel(speed, errorsCount, elapsedTime, numbersCount),
        exercise: exercise,
        speed: speed,
        errorsCount: errorsCount,
        elapsedTime: elapsedTime,
        score: score,
        numbersCount: numbersCount
    };
    isModalVisible.value = true;
};

const handleCurrentCharacter = (character: string) => {
    currentCharacter.value = character;
};

const toggleKeyboardVisibility = (value: boolean) => {
    showKeyboard.value = value;
};
</script>

<template>
    <div class="container">
        <NavigationBarForTrainee></NavigationBarForTrainee>
        <div class="content">
            <div>
                <TypingTrainer level="0" exercise="0" :maxErrors="exerciseData!.errorsCount" :textToType="textToType"
                    customStyleForTrainingField="width: 1378px; height: 140px; border-radius: 20px; font-size: 48px;"
                    @success-completion="handleSuccessCompletion" @error-completion="handleErrorCompletion"
                    @current-charrecter="handleCurrentCharacter" />
                <div class="checkbox-container">
                    <BaseCheckbox label="Отображение виртуальной клавиатуры" :modelValue="showKeyboard"
                        customStyle="font-size: 32px; color: #012E4A; font-family: 'Alegreya Sans SC';"
                        @update:modelValue="toggleKeyboardVisibility" />
                </div>
            </div>
            <Keyboard v-if="showKeyboard" class="keyboard" :currentCharacter="currentCharacter" />
            <FinishExerciseWindow :isVisible="isModalVisible" :levelName="resultData!.level"
                :exerciseName="resultData!.exercise" :wpm="resultData!.speed" :errorsMade="resultData!.errorsCount"
                :allowedErrors="exerciseData.errorsCount" :timeSpent="resultData!.elapsedTime"
                :score="resultData!.score">
            </FinishExerciseWindow>
        </div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-top: 50px;
}

.typing-trainer {
    margin-bottom: 20px;
}

.checkbox-container {
    margin-top: 20px;
}

.keyboard {
    margin-top: 20px;
}
</style>