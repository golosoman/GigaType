<template>
    <a :href="href" :style="customStyle" class="baseButtonBody baseButtonText">
        <slot></slot>
    </a>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'BaseLink',
    props: {
        href: {
            type: String,
            required: true
        },
        customStyle: {
            type: String,
            required: false,
            default: ''
        }
    },
    methods: {
        handleClick(event: MouseEvent) {
            // Здесь можно добавить дополнительную логику, если нужно
            // Например, предотвращение перехода по ссылке при выполнении определенных условий
        }
    }
});
</script>

<style scoped>
.baseButtonBody {
    border: none;
    background-color: #81BECE;
    opacity: 0.8;
    cursor: pointer;
    transition: background-color 0.3s, opacity 0.3s, transform 0.1s;
    text-decoration: none;
    /* Убираем подчеркивание для ссылки */
    display: inline-block;
    /* Позволяет задавать ширину и высоту */
    text-align: center;
    /* Выравнивание текста по центру */
    line-height: 50px;
    /* Высота строки для вертикального центрирования текста */
}

.baseButtonBody:hover {
    background-color: #6FA1B6;
    opacity: 1;
}

.baseButtonBody:active {
    background-color: #5B8DA1;
    transform: scale(0.95);
    opacity: 0.9;
}

.baseButtonText {
    color: #012e4a;
    font-family: "Alegreya Sans SC";
    display: block;
    /* Убедитесь, что текст занимает всю ширину ссылки */
}
</style>
