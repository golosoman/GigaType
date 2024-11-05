<script lang="ts">
import { onMounted, ref } from 'vue'
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
        }
    },
    setup() {
        let id = ref('')

        const setUniqId = () => {
            const date = new Date()
            const timestamp = date.getTime()
            const randomString = Math.random().toString(36).substring(7)
            const randomNumber = Math.floor(Math.random() * 10000)
            const uniqueId = `id-${timestamp}-${randomString}-${randomNumber}`
            return uniqueId
        }

        onMounted(() => {
            id.value = setUniqId()
        })

        return { id }
    },
    methods: {
        updateInput(event: { target: { value: any; }; }) {
            this.$emit('update:modelValue', event.target.value)
        }
    }
}
</script>

<template>
    <input
        :value="modelValue"
        @input="updateInput"
        class="baseInputBody baseInputText"
        :id="id"
        :type="inputType"
        :placeholder="inputPlaceholder"
    />
</template>

<style scoped>
    .baseInputBody {
        border-radius: 15px;
        border-width: 0;
        background-color: #81BECE;
        outline: none;
    }

    .baseInputText {
        font-family: var(--font-family);
        color: #012e4a;
    }

    .baseInputText::placeholder {
        color:#012e4a88;
    }
</style>