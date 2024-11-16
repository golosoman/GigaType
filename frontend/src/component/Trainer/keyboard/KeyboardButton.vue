<template>
    <div :style="customStyle" class="keyboard-button" @click="handleClick">
        <div class="button-content">
            <div v-if="values.length === 2" class="left-value" :style="styleForTwoItem">
                <span>{{ values[0] }}</span>
                <span>{{ values[1] }}</span>
            </div>
            <div v-else class="single-value" :style="styleForOneItem">
                <span>{{ values[0] }}</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'KeyboardButton',
    props: {
        values: {
            type: Array as () => string[],
            required: true,
        },
        onClick: {
            type: Function,
            default: () => { },
        },
        customStyle: {
            type: String,
            required: false,
            default: '',
        },
        styleForOneItem: {
            type: String,
            required: false,
            default: '',
        },
        styleForTwoItem: {
            type: String,
            required: false,
            default: '',
        }
    },
    setup(props) {
        const handleClick = () => {
            if (props.values.length > 0) {
                props.onClick(props.values[0]); // Вызываем первое значение при клике
            }
        };

        return {
            handleClick,
        };
    },
});
</script>

<style scoped>
.keyboard-button {
    border: 2px solid;
    cursor: pointer;
    margin: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: background-color 0.3s;
}

.button-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
}

.left-value {
    display: flex;
    flex-direction: column;
    width: 100%;
    text-align: left;
}

.single-value {
    width: 100%;
    text-align: center;
}
</style>