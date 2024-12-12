<template>
    <nav class="navigation-bar">
        <div style="margin-left: 26px">
            <BaseLogo :logoSrc="logoUrl" customStyleForText="color: #012E4A; font-family: 'Alata'; font-size: 36px;"
                customStyleForImg="width: 91px; height: 82px;">
            </BaseLogo>
        </div>
        <div class="nav-links">
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" :href="trainerLink">Тренажер
            </BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" href="/app/choose_exercise">
                Упражнения</BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" href="/app/trainer">Тестовое
                задание
            </BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" href="/app/information/system">О
                системе</BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" href="/app/information/developer">О
                разработчиках
            </BaseLink>
            <ImageLink url="/app/cabinet/trainee" :imageSrc="userUrl" altText="ЛК"
                customStyle="width: 58px; height: 58px; border-radius: 15px; background-color: #81BECE;" />
        </div>
    </nav>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import BaseLogo from '../logo/BaseLogo.vue';
import { BaseLink, ImageLink } from "@/component/UI";
import LogoUrl from '@/assets/Logo.png';
import UserUrl from '@/assets/User.png';

interface DifficultyLevel {
    name: string;
    uid: string;
    min_length: number;
    max_length: number;
    key_press_time: number;
    max_mistakes: number;
    zones: { keys: string; uid: string }[];
    tasks: Task[];
}

interface Task {
    name: string;
    content: string;
    difficulty_id: string;
    uid: string;
}

export default defineComponent({
    name: 'NavigationBar',
    components: {
        BaseLogo,
        BaseLink,
        ImageLink,
    },
    setup() {
        const logoUrl = ref(LogoUrl);
        const userUrl = ref(UserUrl);
        const trainerLink = ref('/app/trainer'); // Ссылка по умолчанию

        const fetchDifficultyAndTasks = async () => {
            const selectedLevelId = localStorage.getItem('selectedLevelId');
            const selectedTaskId = localStorage.getItem('selectedTaskId');

            if (selectedLevelId && selectedTaskId) {
                // Если оба значения есть, формируем ссылку
                trainerLink.value = `/app/trainer/${selectedLevelId}/${selectedTaskId}`;
            } else {
                // Если нет, запрашиваем уровень сложности
                try {
                    const response = await fetch('/api/difficulty/get');
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const data: DifficultyLevel[] = await response.json();

                    // Находим уровень сложности и задание
                    const levelWithTasks = data.find(level => level.tasks.length > 0);

                    if (levelWithTasks && levelWithTasks.tasks.length > 0) {
                        // Если нашел уровень с заданиями, берем первое задание
                        const taskId = levelWithTasks.tasks[0].uid;
                        localStorage.setItem('selectedLevelId', levelWithTasks.uid);
                        localStorage.setItem('selectedTaskId', taskId);
                        trainerLink.value = `/app/trainer/${levelWithTasks.uid}/${taskId}`;
                    } else {
                        // Если заданий нет, перенаправляем на страницу выбора упражнений
                        window.location.href = '/app/choose_exercise';
                    }
                } catch (error) {
                    console.error('Ошибка при получении уровней сложности:', error);
                }
            }
        };

        onMounted(() => {
            fetchDifficultyAndTasks();
        });

        return { logoUrl, userUrl, trainerLink };
    }
});
</script>

<style scoped>
.for-link {
    width: 254;
    height: 57;
}

.navigation-bar {
    display: flex;
    align-items: center;
    background-color: #378BA4;
    border-radius: 30px;
    padding-top: 8px;
    padding-bottom: 8px;
}

.nav-links {
    display: flex;
    align-items: center;
    font-size: 32px;
    margin-right: 10px;
}

.nav-links>* {
    margin: 0 10px;
}
</style>
