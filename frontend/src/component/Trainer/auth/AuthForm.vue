<script lang="ts">
import { BaseLogo } from "../logo";
import { BaseInputWithLabel, BaseButton, BaseLink } from "@/component/UI";
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'AuthForm',
    components: {
        BaseButton,
        BaseLogo,
        BaseInputWithLabel,
        BaseLink
    },
    props: {
        login: {
            type: [String, Number],
            required: true,
        },
        password: {
            type: [String, Number],
            required: true,
        },
        customStyle: {
            type: String,
            required: false,
            default: '',
        },
    },
    setup(props, { emit }) {
        const changePassword = (password: String) => {
            emit('update:password', password)
        }

        const changeLogin = (login: String) => {
            emit('update:login', login)
        }

        return { changePassword, changeLogin }
    }
})
</script>

<template>
    <div>
        <div class="formContent" :style="customStyle">
            <div>
                <form @submit.prevent>
                    <div class=" formGroup">
                        <BaseInputWithLabel label="Логин" inputPlaceholder="Введите логин:" :modelValue="login"
                            @update:modelValue="changeLogin" style="margin-top: 46px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
                            customStyleForLabel="font-size: 32px;">
                        </BaseInputWithLabel>
                        <BaseInputWithLabel label="Пароль" inputPlaceholder="Введите пароль:" :modelValue="password"
                            inputType="password" @update:modelValue="changePassword" style="margin-top: 38px;"
                            customStyleForInput="width: 450px; height: 57px; font-size: 32px;"
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
.headerButton {
    display: flex;
}

.formContent {
    width: 502px;
    height: 435px;
    background-color: #D9E1E5;
}

.formGroup {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>