<template>
    <div class="keyboard" :style="customStyle">
        <div v-for="(row, rowIndex) in keys" :key="rowIndex" class="keyboard-row">
            <KeyboardButton v-for="(key, keyIndex) in row" :key="keyIndex" :values="Array.isArray(key) ? key : [key]"
                :onClick="handleButtonClick" :style="{ backgroundColor: getKeyColor(key) }"
                :customStyle="getButtonStyle(key)" styleForOneItem="font-size: 40px;"
                styleForTwoItem="font-size: 22px; margin-left: 10px; margin-bottom: 5px;" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import KeyboardButton from './KeyboardButton.vue';
import { KeyboardZones } from '../util';

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
            [KeyboardZones.ZONE_1]: ['ф', 'ы', 'в', 'а', 'о', 'л', 'д', 'ж'],
            [KeyboardZones.ZONE_2]: ['п', 'р'],
            [KeyboardZones.ZONE_3]: ['к', 'е', 'н', 'г'],
            [KeyboardZones.ZONE_4]: ['м', 'и', 'т', 'ь'],
            [KeyboardZones.ZONE_5]: ['у', 'с', 'ш', 'б'],
            [KeyboardZones.ZONE_6]: ['ц', 'ч', 'щ', 'ю'],
            [KeyboardZones.ZONE_7]: ['ё', 'й', 'я', 'з', 'х', 'ъ', 'э', '.', ','],
            [KeyboardZones.ZONE_8]: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            [KeyboardZones.ZONE_9]: ['!', '"', '№', ';', '%', ':', '?', '*', '(', ')', '_', '-', '+', '='],
            [KeyboardZones.ZONE_10]: [' '],
        };

        // Маппинг зон на цвета
        const zoneColors: Record<string, string> = {
            [KeyboardZones.ZONE_1]: '#FFCCCB',
            [KeyboardZones.ZONE_2]: '#FFD700',
            [KeyboardZones.ZONE_3]: '#ADFF2F',
            [KeyboardZones.ZONE_4]: '#00FA9A',
            [KeyboardZones.ZONE_5]: '#00BFFF',
            [KeyboardZones.ZONE_6]: '#FF69B4',
            [KeyboardZones.ZONE_7]: '#BA55D3',
            [KeyboardZones.ZONE_8]: '#6495ED',
            [KeyboardZones.ZONE_9]: '#E24548',
            [KeyboardZones.ZONE_10]: '#90EE90'
        };

        const handleButtonClick = (value: string) => {
            console.log('Clicked:', value);
            // Здесь вы можете обрабатывать нажатие кнопки
        };

        const getButtonStyle = (key: string | string[]): string => {
            const baseStyle = 'background-color: #E8EDE7; width: 50px; height: 50px; font-size: 25px; border-radius: 10px;';
            if (key.includes(' ')) {
                return `${baseStyle} width: 350px; height: 50px; font-size: 25px;`; // Увеличенная ширина для пробела
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
