<template>
    <div class="base-image" :style="customStyle">
        <img :src="src" :alt="alt" @load="handleLoad" @error="handleError" class="image" />
        <div v-if="loading" class="loading">Загрузка...</div>
        <div v-if="error" class="error">Ошибка загрузки изображения</div>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from 'vue'
const props = defineProps<{
    src: string;
    alt?: string;
    loadingText?: string;
    customStyle?: string;
}>();

const loading = ref(true);
const error = ref(false);

const handleLoad = () => {
    loading.value = false;
};

const handleError = () => {
    loading.value = false;
    error.value = true;
};
</script>

<style scoped>
.base-image {
    position: relative;
    display: inline-block;
}

.image {
    display: block;
    max-width: 100%;
    height: auto;
}

.loading,
.error {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 16px;
    color: #777;
}
</style>