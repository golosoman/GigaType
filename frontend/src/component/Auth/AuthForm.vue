<script lang="ts">
import { BaseInputWithLabel, BaseButton, BaseLogo } from "../UI";
import { defineComponent } from 'vue';

export default defineComponent({
    components: {
        BaseButton,
        BaseLogo,
        BaseInputWithLabel
    },
    props: {
        login: {
            type: [String, Number],
            required: true,
        },
        password: {
            type: [String, Number],
            required: true,
        }
    },
    emits: ['update:password', 'update:login'],
    methods: {
        changePassword(password: String) {
            this.$emit('update:password', password) // previously was `this.$emit('input', title)`
        },
        changeLogin(login: String) {
            this.$emit('update:login', login) // previously was `this.$emit('input', title)`
        },
    }
})
</script>

<template>
    <div>
        <div class="formContent">
            <div>
                <BaseButton
                    customStyle="width: 251px; height: 61px; background-color: #012E4A; color: #E8EDE7; text-align: left; font-size: 32px;">
                    Вход
                </BaseButton>
                <BaseButton customStyle="width: 251px; height: 61px; text-align: left; font-size: 32px;">Регистрация
                </BaseButton>
            </div>
            <div>
                <form @submit.prevent>
                    <div class="formGroup">
                        <BaseInputWithLabel label="Логин" :modelValue="login" @update:modelValue="changeLogin"
                            style="margin-top: 46px;" customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <BaseInputWithLabel label="Пароль" :modelValue="password" @update:modelValue="changePassword"
                            style="margin-top: 38px;" customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <BaseButton
                            customStyle="width: 171px; height: 57px; border-radius: 15px; margin-top: 41px; font-size: 32px; color: #012E4A;">
                            Войти
                        </BaseButton>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.formContent {
    width: 502px;
    height: 496px;
    background-color: #D9E1E5;
}

.formGroup {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>