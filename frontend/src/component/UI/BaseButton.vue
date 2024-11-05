<script lang="ts">
export default {
  props: {
  }
}
</script>

<template>
    <button class="baseButtonBody baseButtonText">
        <slot></slot>
    </button>
</template>


<style scoped>
    .baseButtonBody {
        border-radius: 15px;
        border-width: 0;
        background-color: #81BECE;
        opacity: 0.8;
    }

    .baseButtonText {
        text-align: center;
        color: #012e4a;
        --font-family: "Alegreya Sans SC", sans-serif;
        --second-family: "Alata", sans-serif;
    }
</style>