<template>
    <div class="logoContainer">
        <img src="@/assets/logo.jpg" alt="Логотип" class="logoImg" :style="customStyleForImg" />
        <span class="logoText" :style="customStyleForText">GIGATYPE</span>
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
.logoContainer {
    position: relative;
}

.logoImg {
    max-width: 100%;
    height: auto;
}

.logoText {
    font-family: "Alata";
    color: #012E4A;
}
</style>