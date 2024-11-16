<template>
    <div class="content">
        <NavigationBarForTrainee></NavigationBarForTrainee>
        <div style="margin-left: 60px;">
            <div class="container">
                <div>
                    <BaseImage :src="UserImage"
                        customStyle="background-color: #81BECE; border-radius: 30px; width: 300px; height: 300px; margin-top: 40px;">
                    </BaseImage>
                </div>

                <div class="input-container">
                    <BaseInputWithLabel v-model="userName" label="Пользователь"
                        customStyleForInput="width: 450px; height: 57px; font-size: 32px; pointer-events: none;"
                        customStyleForLabel="font-size: 32px; pointer-events: none;">
                    </BaseInputWithLabel>
                </div>

            </div>
            <div>
                <BaseButton
                    customStyle="width: 35s0px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
                    Изменить фотографию
                </BaseButton>
            </div>
            <div>
                <h2>Статистика</h2>
                <div>
                    <BaseButton
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A;">
                        Скорость</BaseButton>
                    <BaseButton
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A; margin-left: 20px;">
                        Уровни</BaseButton>
                    <BaseButton
                        customStyle="width: 254px; height: 57px; border-radius: 15px; font-size: 32px; color: #012E4A; margin-left: 20px;">
                        Обучаемые</BaseButton>
                </div>
                <div>
                    <h2>Таблица рейтинга</h2>
                    <RatingTable :user-data="userData" custom-style="width: 500px"></RatingTable>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { NavigationBarForTrainee } from '@/component/trainer';
import { BaseImage, BaseButton, BaseInputWithLabel } from '@/component/UI';
import { RatingTable } from '@/component/statistic';
import UserImage from '@/assets/User.png'
import { ref } from 'vue'

const userName = ref('trainee')

const userData = ref([
    { Место: 1, Пользователь: 'Иван', Рейтинг: 1500 },
    { Место: 2, Пользователь: 'Анна', Рейтинг: 1450 },
    { Место: 3, Пользователь: 'Петр', Рейтинг: 1400 },
    { Место: 4, Пользователь: 'Светлана', Рейтинг: 1350 },
    { Место: 5, Пользователь: 'Дмитрий', Рейтинг: 1300 },
]);
</script>

<style scoped>
.content {
    display: flex;
    flex-direction: column;
}

.container {
    display: flex;
    align-items: flex-start;
    margin-top: 20px;
}

.input-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 50px;
    margin-top: 50px;
}

.BaseImage {
    margin-top: 40px;
}
</style>