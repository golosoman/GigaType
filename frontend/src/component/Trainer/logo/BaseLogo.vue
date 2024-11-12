<template>
    <div class="content">
        <div class="logoContainer">
            <img :src="logoSrc" alt="Логотип" class="logoImg" :style="customStyleForImg" />
            <span class="logoText" :style="customStyleForText">GIGATYPE</span>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'BaseLogo',
    props: {
        logoSrc: {
            type: String,
            required: true
        },
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
}

.logoContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.logoText {
    font-family: "Alata";
    color: #012E4A;
    margin-top: 8px;
}
</style>
