<template>
    <a :href="url" class="image-link" :style="customStyle" target="_blank" rel="noopener noreferrer">
        <img :src="imageSrc" :alt="altText" class="image" />
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
}

.image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
</style>
