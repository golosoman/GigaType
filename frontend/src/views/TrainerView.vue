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
}
const isModalVisible = ref(false);
const resultData = ref<CompletionData>({
    level: "",
    exercise: "",
    speed: 0,
    errorsCount: 0,
    elapsedTime: 0,
    score: 0
});
const showKeyboard = ref(false);
const currentCharacter = ref('');

const handleSuccessCompletion = (data: any[]) => {
    resultData.value = {
        level: data[0],
        exercise: data[1],
        speed: data[2],
        errorsCount: data[3],
        elapsedTime: data[4],
        score: data[5],
    };
    isModalVisible.value = true
};

const handleErrorCompletion = (data: any[]) => {
    resultData.value = {
        level: data[0],
        exercise: data[1],
        speed: data[2],
        errorsCount: data[3],
        elapsedTime: data[4],
        score: data[5],
    };
    isModalVisible.value = true
};

const handleCurrentCharacter = (character: string) => {
    currentCharacter.value = character;
}

const toggleKeyboardVisibility = (value: boolean) => {
    showKeyboard.value = value;
};
</script>

<template>
    <div class="container">
        <NavigationBarForTrainee></NavigationBarForTrainee>
        <div class="content">
            <div>
                <TypingTrainer level="Легкий" exercise="Печать текста" :maxErrors="5"
                    textToType="Пример текста для тренировки. 1234567890,()"
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
                :allowedErrors="5" :timeSpent="resultData!.elapsedTime" :score="resultData!.score">
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
