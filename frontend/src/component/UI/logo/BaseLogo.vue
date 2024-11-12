<template>
    <div class="content">
        <div class="logoContainer">
            <img src="@/assets/logo.png" alt="Логотип" class="logoImg" :style="customStyleForImg" />
            <span class="logoText" :style="customStyleForText">GIGATYPE</span>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'BaseLogo',
    props: {
        customStyleForImg: {
            type: String,
            default: ''
        },
        customStyleForText: {
            type: String,
            default: ''
        },
    }
});
</script>

<style scoped>
.content {
    display: flex;
    align-items: flex-start;
    /* Выравнивание по верхнему краю для родительского контейнера */
}

.logoContainer {
    display: flex;
    flex-direction: column;
    /* Устанавливаем направление колонкой */
    align-items: center;
    /* Центрируем элементы по горизонтали внутри logoContainer */
}

.logoImg {
    mix-blend-mode: color;
}

.logoText {
    font-family: "Alata";
    color: #012E4A;
    margin-top: 8px;
    /* Отступ между изображением и текстом */
}
</style>
