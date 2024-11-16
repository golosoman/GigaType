<template>
    <div class="keyboard">
        <div v-for="(row, rowIndex) in keys" :key="rowIndex" class="keyboard-row">
            <KeyboardButton v-for="(key, keyIndex) in row" :key="keyIndex" :values="Array.isArray(key) ? key : [key]"
                :onClick="handleButtonClick" :customStyle="getButtonStyle(key)" styleForOneItem="font-size: 50px;"
                styleForTwoItem="font-size: 27px; margin-left: 10px; margin-bottom: 5px;" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import KeyboardButton from './KeyboardButton.vue';

export default defineComponent({
    name: 'Keyboard',
    components: {
        KeyboardButton,
    },
    props: {
        currentCharacter: {
            type: String,
            required: false,
            default: null,
        },
    },
    setup(props) {
        const currentCharacter = ref(props.currentCharacter);
        watch(() => props.currentCharacter, (newValue) => {
            currentCharacter.value = newValue;
        });

        const keys = ref([
            [['ё'], ['1', '!'], ['2', '"'], ['3', '№'], ['4', ';'], ['5', '%'], ['6', ':'], ['7', '?'], ['8', '*'], ['9', '('], ['0', ')'], ['_', '-'], ['+', '=']],
            [['й'], ['ц'], ['у'], ['к'], ['е'], ['н'], ['г'], ['ш'], ['щ'], ['з'], ['х'], ['ъ']],
            [['ф'], ['ы'], ['в'], ['а'], ['п'], ['р'], ['о'], ['л'], ['д'], ['ж'], ['э']],
            [['я'], ['ч'], ['с'], ['м'], ['и'], ['т'], ['ь'], ['б'], ['.', ',']],
            [[' ']]
        ]);

        const handleButtonClick = (value: string) => {
            console.log('Clicked:', value);
            // Здесь вы можете обрабатывать нажатие кнопки
        };

        const getButtonStyle = (key: string | string[]): string => {
            // Проверяем, совпадает ли с текущим символом
            const isActive = Array.isArray(key) ? key[0] === currentCharacter.value.toLowerCase() || key[1] === currentCharacter.value.toLowerCase() : key;

            const baseStyle = 'background-color: #E8EDE7; width: 60px; height: 60px; font-size: 30px; border-radius: 10px;';
            const activeStyle = 'background-color: orange;'; // Оранжевый цвет для активной кнопки

            // Проверяем, является ли ключ пробелом
            if (key.includes(' ')) {
                return `${baseStyle} width: 400px; height: 60px; font-size: 30px; ${isActive ? activeStyle : ''}`; // Увеличенная ширина для пробела
            }
            return `${baseStyle} ${isActive ? activeStyle : ''}`; // Стандартный стиль
        };

        return {
            keys,
            currentCharacter,
            handleButtonClick,
            getButtonStyle,
        };
    },
});
</script>

<style scoped>
.keyboard {
    display: flex;
    flex-direction: column;
}

.keyboard-row {
    display: flex;
    justify-content: center;
}
</style>