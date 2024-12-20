<template>
    <nav class="navigation-bar">
        <div style="margin-left: 26px">
            <BaseLogo :logoSrc="logoUrl" customStyleForText="color: #012E4A; font-family: 'Alata'; font-size: 36px;"
                customStyleForImg="width: 91px; height: 82px; ">
            </BaseLogo>
        </div>
        <div class="nav-links">
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" href="/app/edit/level">Редактор
                уровня
            </BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" class="for-link"
                href="/app/edit/exercise">
                Редактор упражнения</BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px;; border-radius: 15px;" class="for-link"
                href="/app/edit/user">Редактор
                пользователей</BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" href="/public/AboutSystem.html">О
                системе</BaseLink>
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;"
                href="/public/AboutDevelopers.html">О
                разработчиках
            </BaseLink>
            <ImageLink url="/app/cabinet/admin" :imageSrc="userUrl" altText="ЛК"
                customStyle="width: 58px; height: 58px; border-radius: 15px; background-color: #81BECE;" />
        </div>
    </nav>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import BaseLogo from '../logo/BaseLogo.vue';
import { BaseLink, ImageLink } from "@/component/UI";
import LogoUrl from '@/assets/Logo.png'
import UserUrl from '@/assets/User.png'


export default defineComponent({
    name: 'NavigationBar',
    components: {
        BaseLogo,
        BaseLink,
        ImageLink,
    },
    setup(props) {
        const logoUrl = ref(LogoUrl);
        const userUrl = ref(UserUrl);
        return { logoUrl, userUrl }
    }
});
</script>

<style scoped>
.for-link {
    /* высота кнопки */
    /* убираем отступы */
    text-align: center;
    /* выравнивание текста влево */
    line-height: 20px;
    /* устанавливаем высоту строки меньше высоты кнопки */
    display: flex;
    /* используем flexbox для управления выравниванием */
    align-items: center;
    /* выравнивание по верхнему краю */
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
