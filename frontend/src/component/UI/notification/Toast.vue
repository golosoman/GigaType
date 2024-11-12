<template>
    <transition name="fade">
        <div v-if="visible" class="toast" :class="type">
            <span>{{ message }}</span>
            <button class="close-button" @click="closeToast">×</button>
        </div>
    </transition>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';

export default defineComponent({
    name: 'Toast',
    props: {
        modelValue: {
            type: Boolean,
            required: true,
        },
        message: {
            type: String,
            required: true,
        },
        type: {
            type: String,
            default: 'info', // может быть error, success, warning и т.д.
        },
        duration: {
            type: Number,
            default: 3000, // продолжительность отображения в миллисекундах
        },
    },
    setup(props, { emit }) {
        const visible = ref(props.modelValue);
        let timer: ReturnType<typeof setTimeout>;

        const closeToast = async () => {
            visible.value = false;
            await nextTick(); // Ждем следующего обновления
            emit('update:modelValue', false); // Уведомляем родительский компонент
            clearTimeout(timer);
        };

        onMounted(() => {
            timer = setTimeout(() => {
                closeToast(); // Вызываем closeToast для плавного исчезновения
            }, props.duration);
        });

        onBeforeUnmount(() => {
            clearTimeout(timer);
        });

        // Наблюдаем за изменением modelValue и обновляем видимость
        watch(() => props.modelValue, (newValue) => {
            visible.value = newValue;
        });

        return { visible, closeToast };
    },
});
</script>

<style scoped>
.toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 15px;
    border-radius: 5px;
    color: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
}

.toast.info {
    background-color: #2196F3;
}

.toast.error {
    background-color: #f44336;
}

.toast.success {
    background-color: #4CAF50;
}

.toast.warning {
    background-color: #FF9800;
}

.close-button {
    background: none;
    border: none;
    color: white;
    font-size: 20px;
    cursor: pointer;
    margin-left: 15px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>