<script setup lang="ts">
const vModel = defineModel<'dark' | 'light'>({ required: true });

const { size = 40 } = defineProps<{
    size?: number;
}>();

const toogle = () => {
    if (vModel.value == 'light') {
        vModel.value = 'dark';
    } else {
        vModel.value = 'light';
    }
};
</script>

<template>
    <button
        type="button"
        :class="[$style.button, $style[vModel], $style[`size_${size}`]]"
        :style="{ width: `${size}px`, height: `${size}px` }"
        :title="vModel == 'light' ? 'Светлая тема' : 'Тёмная тема'"
        @click="toogle"
    >
        <span>
            <span :class="$style.day"></span>
            <span :class="$style.night"></span>
        </span>
    </button>
</template>

<style lang="less" module>
@import '@styles/includes';

.button {
    text-decoration: none;
    display: block;
    position: relative;
    overflow: hidden;
    border-radius: 100%;
    background-color: var(--color-2);
    transition: background-color 0.25s ease;
    -webkit-tap-highlight-color: transparent;

    .hover({
        background-color: var(--color-2-hover);
    });

    > span {
        display: flex;
        position: absolute;
        top: 0;
        left: 0;
        width: 200%;
        height: 100%;
        transition: all 0.5s !important;
        transform: translateX(0px);

        > span {
            display: block;
            flex-basis: 50%;
            background-color: var(--stable-white-color);
        }

        > .day {
            mask: url('@/assets/icons/sun_20.svg') no-repeat center center;
            mask-size: 20px auto;
        }

        > .night {
            mask: url('@/assets/icons/moon_20.svg') no-repeat center center;
            mask-size: 20px auto;
        }
    }

    &.dark {
        > span {
            transform: translateX(-50%);
        }
    }

    &.size_30 {
        > span {
            > .day {
                mask-size: 16px auto;
            }

            > .night {
                mask-size: 16px auto;
            }
        }
    }
}
</style>
