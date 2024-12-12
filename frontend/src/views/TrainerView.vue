<script setup lang="ts">
import { Keyboard, TypingTrainer, NavigationBarForTrainee, FinishExerciseWindow } from '@/component/trainer';
import { BaseCheckbox } from '@/component/UI';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

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
    exercise: "",
    speed: 0,
    errorsCount: 0,
    elapsedTime: 0,
    score: 0,
    numbersCount: 0
});

const exerciseData = ref<CompletionData>({
    level: "",
    exercise: "",
    speed: 0,
    errorsCount: 0,
    elapsedTime: 0,
    score: 0,
    numbersCount: 0
});
const showKeyboard = ref(false);
const currentCharacter = ref(' ');
const textToType = ref(''); // Для хранения текста для печати

const route = useRoute();

const fetchDifficultyData = async (difficultyId: string) => {
    try {
        const response = await axios.get(`/api/difficulty/get?uid=${difficultyId}`);
        const difficultyInfo = response.data[0];
        console.log(difficultyInfo)
        return {
            name: difficultyInfo.name,
            min_length: difficultyInfo.min_length,
            max_length: difficultyInfo.max_length,
            key_press_time: difficultyInfo.key_press_time,
            max_mistakes: difficultyInfo.max_mistakes,
        };
    } catch (error) {
        console.error("Ошибка при получении данных о сложности:", error);
    }
};

const fetchTaskData = async (taskId: string) => {
    try {
        const response = await axios.get(`/api/task/get?uid=${taskId}`);
        const taskInfo = response.data[0];
        console.log(taskInfo)
        return {
            name: taskInfo.name,
            content: taskInfo.content,
        };
    } catch (error) {
        console.error("Ошибка при получении данных о задаче:", error);
    }
};

const sendCompletionData = async (success: boolean) => {
    const taskUid = route.params.exerciseId; // id упражнения из URL
    const data = {
        task_uid: taskUid,
        used_time: resultData.value.elapsedTime,
        mistakes: resultData.value.errorsCount,
        clicks_number: resultData.value.numbersCount, // Замените на реальное количество нажатий, если нужно
        success: success,
        score: resultData.value.score,
    };

    try {
        await axios.post('/api/stat/create', data);
        console.log("Данные успешно отправлены на сервер:", data);
    } catch (error) {
        console.log(`${data} - данные все сломали`)
        console.error("Ошибка при отправке данных на сервер:", error);
    }
};

onMounted(async () => {
    const { params } = route;
    const levelId = params.levelId; // id уровня сложности из URL
    const exerciseId = params.exerciseId; // id упражнения из URL
    console.log(params)

    const difficultyData = await fetchDifficultyData(levelId);
    const taskData = await fetchTaskData(exerciseId);

    if (difficultyData && taskData) {
        exerciseData.value.level = difficultyData.name;
        exerciseData.value.exercise = taskData.name;
        exerciseData.value.errorsCount = difficultyData.max_mistakes;
        exerciseData.value.elapsedTime = difficultyData.key_press_time;
        textToType.value = taskData.content; // Устанавливаем текст для печати
    }
});

const handleSuccessCompletion = (data: any[]) => {
    resultData.value = {
        level: data[0],
        exercise: data[1],
        speed: data[2],
        errorsCount: data[3],
        elapsedTime: data[4],
        score: data[5],
        numbersCount: data[6]
    };
    isModalVisible.value = true;
    sendCompletionData(true); // Отправляем данные с успехом
};

const handleErrorCompletion = (data: any[]) => {
    resultData.value = {
        level: data[0],
        exercise: data[1],
        speed: data[2],
        errorsCount: data[3],
        elapsedTime: data[4],
        score: data[5],
        numbersCount: data[6]
    };
    isModalVisible.value = true;
    sendCompletionData(false); // Отправляем данные с ошибкой
};

const handleCurrentCharacter = (character: string) => {
    console.log("Новый символ" + character)
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
                <TypingTrainer :level="exerciseData!.level" :exercise="exerciseData!.exercise"
                    :maxErrors="exerciseData!.errorsCount" :textToType="textToType"
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
