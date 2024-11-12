<template>
    <a :href="url" class="image-link" :style="customStyle" target="_blank" rel="noopener noreferrer">
        <img :src="imageSrc" :alt="altText" class="image-link__image" />
    </a>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'ImageLink',
    props: {
        url: {
            type: String,
            required: true,
        },
        imageSrc: {
            type: String,
            required: true,
        },
        altText: {
            type: String,
            default: 'Image',
        },
        customStyle: {
            type: String,
            required: false,
            default: ''
        },
    },
});
</script>

<style scoped>
.image-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: inherit;
    /* Убираем цвет ссылки, чтобы использовать цвет текста */
}

.image-link__image {
    max-width: 50px;
    /* Устанавливаем максимальную ширину для изображения */
    margin-right: 8px;
    /* Отступ между изображением и текстом */
}
</style>