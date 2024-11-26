<template>
    <button class="button-with-image" @click="handleClick" :style="customStyle">
        <img :src="imageSrc" :alt="imageAlt" class="button-image" :style="customStyleForImage" />
        <span class="button-text" :style="customStyleForText">{{ text }}</span>
    </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'ButtonWithImage',
    props: {
        imageSrc: {
            type: String,
            required: true,
        },
        imageAlt: {
            type: String,
            default: 'Button image',
        },
        text: {
            type: String,
            required: false,
            default: ''
        },
        customStyle: {
            type: String,
            required: false,
            default: ''
        },
        customStyleForImage: {
            type: String,
            required: false,
            default: ''
        },
        customStyleForText: {
            type: String,
            required: false,
            default: ''
        }
    },
    setup(props, { emit }) {
        const handleClick = () => {
            emit('click');
        };

        return {
            handleClick,
        };
    },
});
</script>

<style scoped>
.button-with-image {
    display: flex;
    align-items: center;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background-color: violet;
}

.button-text {
    margin-left: 2px;
}
</style>