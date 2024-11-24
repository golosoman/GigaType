<template>
    <div class="keyboard" :style="customStyle">
        <div v-for="(row, rowIndex) in keys" :key="rowIndex" class="keyboard-row">
            <KeyboardButton v-for="(key, keyIndex) in row" :key="keyIndex" :values="Array.isArray(key) ? key : [key]"
                :onClick="handleButtonClick" :style="{ backgroundColor: getKeyColor(key) }"
                :customStyle="getButtonStyle(key)" styleForOneItem="font-size: 50px;"
                styleForTwoItem="font-size: 27px; margin-left: 10px; margin-bottom: 5px;" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import KeyboardButton from './KeyboardButton.vue';

export default defineComponent({
    name: 'KeyboardForZone',
    components: {
        KeyboardButton,
    },
    props: {
        selectedZones: {
            type: Array as () => string[],
            required: false,
            default: () => []
        },
        customStyle: {
            type: String,
            required: false,
            default: '',
        },
    },
    setup(props) {
        const keys = ref([
            [['ё'], ['1', '!'], ['2', '"'], ['3', '№'], ['4', ';'], ['5', '%'], ['6', ':'], ['7', '?'], ['8', '*'], ['9', '('], ['0', ')'], ['_', '-'], ['+', '=']],
            [['й'], ['ц'], ['у'], ['к'], ['е'], ['н'], ['г'], ['ш'], ['щ'], ['з'], ['х'], ['ъ']],
            [['ф'], ['ы'], ['в'], ['а'], ['п'], ['р'], ['о'], ['л'], ['д'], ['ж'], ['э']],
            [['я'], ['ч'], ['с'], ['м'], ['и'], ['т'], ['ь'], ['б'], ['.', ',']],
            [[' ']]
        ]);

        const zoneMapping: Record<string, string[]> = {
            'Зона 1 (ФЫВАОЛДЖ)': ['ф', 'ы', 'в', 'а', 'о', 'л', 'д', 'ж'],
            'Зона 2 (ПР)': ['п', 'р'],
            'Зона 3 (КЕНГ)': ['к', 'е', 'н', 'г'],
            'Зона 4 (МИТЬ)': ['м', 'и', 'т', 'ь'],
            'Зона 5 (УСШБ)': ['у', 'с', 'ш', 'б'],
            'Зона 6 (ЦЧЩЮ)': ['ц', 'ч', 'щ', 'ю'],
            'Зона 7 (ЁЙЯЗХЪЭ.,)': ['ё', 'й', 'я', 'з', 'х', 'ъ', 'э', '.', ','],
            'Зона 8 (1234567890)': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            'Зона 9 (символы)': ['!', '"', '№', ';', '%', ':', '?', '*', '(', ')', '_', '-', '+', '='],
            'Зона Пробела': [' '],
        };

        // Маппинг зон на цвета
        const zoneColors: Record<string, string> = {
            'Зона 1 (ФЫВАОЛДЖ)': '#FFCCCB',
            'Зона 2 (ПР)': '#FFD700',
            'Зона 3 (КЕНГ)': '#ADFF2F',
            'Зона 4 (МИТЬ)': '#00FA9A',
            'Зона 5 (УСШБ)': '#00BFFF',
            'Зона 6 (ЦЧЩЮ)': '#FF69B4',
            'Зона 7 (ЁЙЯЗХЪЭ.,)': '#BA55D3',
            'Зона 8 (1234567890)': '#6495ED',
            'Зона 9 (символы)': '#E24548',
            'Зона Пробела': '#90EE90'
        };

        const handleButtonClick = (value: string) => {
            console.log('Clicked:', value);
            // Здесь вы можете обрабатывать нажатие кнопки
        };

        const getButtonStyle = (key: string | string[]): string => {
            const baseStyle = 'background-color: #E8EDE7; width: 60px; height: 60px; font-size: 30px; border-radius: 10px;';
            if (key.includes(' ')) {
                return `${baseStyle} width: 400px; height: 60px; font-size: 30px;`; // Увеличенная ширина для пробела
            }
            return `${baseStyle}`; // Стандартный стиль
        };

        const getKeyColor = (key: string[]) => {
            // Проверяем, является ли ключ пробелом
            if (key.includes(' ')) {
                return zoneColors['Зона Пробела']; // Возвращаем цвет для пробела
            }

            for (let i = 0; i < props.selectedZones.length; i++) {
                const zone = props.selectedZones[i];
                if (zoneMapping[zone]) {
                    if (zoneMapping[zone].some(activeKey => key.includes(activeKey))) {
                        return zoneColors[zone]; // Возвращаем цвет для соответствующей зоны
                    }
                }
            }
            return ''; // Если зона не выбрана, возвращаем пустую строку (без цвета)
        };

        return {
            keys,
            getButtonStyle,
            handleButtonClick,
            getKeyColor,
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
