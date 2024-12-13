<script setup lang="ts">
import { Keyboard, TypingTrainer, NavigationBarForTrainee, FinishExerciseWindow } from '@/component/trainer';
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
    exercise: "На краю света, где океан встречается с небом, раскинулись бескрайние просторы. Здесь время останавливается, и каждый вдох наполняется энергией природы. Ветер нежно колышет травы, а волны омывают берег, создавая мелодию, которая звучит в унисон с нашими мечтами. Это место, где мы можем быть собой и забыть о заботах.",
    speed: 0,
    errorsCount: 5, // Максимальное количество ошибок для начального уровня
    elapsedTime: 0,
    score: 0,
    numbersCount: 0
});

const showKeyboard = ref(false);
const currentCharacter = ref(' ');
const textToType = ref("На краю света, где океан встречается с небом, раскинулись бескрайние просторы. Здесь время останавливается, и каждый вдох наполняется энергией природы. Ветер нежно колышет травы, а волны омывают берег, создавая мелодию, которая звучит в унисон с нашими мечтами. Это место, где мы можем быть собой и забыть о заботах."); // Статический текст

const determineLevel = (speed: number, errorsCount: number, elapsedTime: number, totalLength: number): string => {
    // Учитываем ошибки и время, а также процент завершенного задания
    const adjustedSpeed = speed - (errorsCount * 2) - (elapsedTime / 60);
    const completionRate = (totalLength > 0) ? (speed / totalLength) : 0; // Процент введенного текста

    if (completionRate < 0.5) {
        return "Не завершено"; // Если менее 50% текста введено
    } else if (adjustedSpeed < 60) {
        return "Начальный";
    } else if (adjustedSpeed >= 60 && adjustedSpeed <= 120) {
        return "Средний";
    } else if (adjustedSpeed > 120) {
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
                <TypingTrainer :level="exerciseData!.level" exercise="test" :maxErrors="exerciseData!.errorsCount"
                    :textToType="textToType"
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