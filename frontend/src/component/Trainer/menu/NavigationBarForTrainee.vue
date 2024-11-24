<template>
    <nav class="navigation-bar">
        <div style="margin-left: 26px">
            <BaseLogo :logoSrc="logoUrl" customStyleForText="color: #012E4A; font-family: 'Alata'; font-size: 36px;"
                customStyleForImg="width: 91px; height: 82px; ">
            </BaseLogo>
        </div>
        <div class="nav-links">
            <BaseLink customStyle="width: 254px; height: 57px; border-radius: 15px;" href="/app/trainer">Тренажер
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
            <ImageLink url="/app/cabinet" :imageSrc="userUrl" altText="ЛК"
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
