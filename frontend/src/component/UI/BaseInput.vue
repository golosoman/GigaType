<script lang="ts">
import { onMounted, ref } from 'vue';
import { setUniqId } from './util';
export default {
    props: {
        modelValue: {
            type: [String, Number],
            required: true,
            default: ''
        },
        inputPlaceholder: {
            type: String,
            required: true,
            default: 'Ввод: '
        },
        inputType: {
            type: String,
            required: true,
            default: 'text'
        },
        customStyle: { // Новый пропс для стилей
            type: String,
            default: ''
        },
        id: { // Новый пропс для id
            type: String,
            default: ''
        }
    },
    setup(props) {
        const id = ref(props.id || ''); // Используем переданный id или пустую строку
        onMounted(() => {
            if (!id.value) {
                id.value = setUniqId(); // Генерируем уникальный id, если id не был передан
            }
        });
        return { id }
    },
    methods: {
        updateInput(event: Event) {
            const target = event.target as HTMLInputElement; // Приведение типа
            this.$emit('update:modelValue', target.value); // Получаем значение из target
        }
    }
}
</script>
<template>
    <input :value="modelValue" @input="updateInput" class="baseInputBody baseInputText" :id="id" :type="inputType"
        :placeholder="inputPlaceholder" :style="customStyle" />
</template>
<style scoped>
.baseInputBody {
    border-radius: 15px;
    /* Скругление углов */
    border: none;
    /* Убираем границу полностью */
    background-color: #81BECE;
    /* Цвет фона */
    outline: none;
    /* Убираем обводку при фокусировке */
    padding-left: 10px;
    /* Внутренний отступ слева для улучшения читаемости */
    transition: box-shadow 0.3s ease;
    /* Плавный переход для эффекта фокуса */
}

.baseInputBody:focus {
    box-shadow: 0 0 5px #012e4a88;
    /* Эффект фокуса */
}

.baseInputText {
    font-family: "Alegreya Sans SC";
    /* Шрифт */
    color: #012e4a;
    /* Цвет текста */
    border: none;
    /* Убираем границу у текста */
    width: 100%;
    /* Полная ширина для текста */
    outline: none;
    /* Убираем обводку при фокусировке */
}

.baseInputText::placeholder {
    color: #012e4a88;
    /* Цвет плейсхолдера с прозрачностью */
}

.baseInputText:focus {
    color: #012e4a;
    /* Цвет текста при фокусировке */
}
</style>
