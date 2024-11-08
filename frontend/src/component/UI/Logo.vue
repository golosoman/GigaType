<template>
    <img src="@/assets/logo.jpg" alt="Логотип" class="logoImg" />
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
    name: 'Logo'
});
</script>
<style scoped>
.logoImg {
    max-width: 100%;
    /* Адаптивный размер */
    height: auto;
    /* Сохраняет пропорции */
}
</style>