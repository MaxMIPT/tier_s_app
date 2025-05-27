<script setup lang="ts">
import IMask, { type FactoryArg } from 'imask';

const vModel = defineModel<string>({ default: '' });
const props = defineProps<{
    type?: 'text' | 'password' | 'number';
    name?: string;
    min?: number;
    max?: number;
    step?: number;
    placeholder?: string;
    required?: boolean;
    mask?: FactoryArg;
    maskUnlazyOnFocus?: boolean;
    isError?: boolean;
    readValueFromVModelOnBlur?: boolean;
}>();

const emit = defineEmits(['maskComplete', 'maskAccept']);

const inputRef = ref<HTMLInputElement | null>(null);
let maskObject: ReturnType<typeof IMask> | null = null;
const inputValue = ref<string | number>(vModel.value);

const maskIsComplete = ref(false);
const maskRawInputValue = ref('');

const isFocused = ref(false);

onMounted(() => {
    if (inputRef.value) {
        if (props.mask) {
            maskObject = IMask(inputRef.value, props.mask);
            maskObject.on('accept', () => {
                if (!maskObject) return;
                maskIsComplete.value = false;
                maskRawInputValue.value = maskObject.rawInputValue;
                inputValue.value = maskObject.value;
                emit('maskAccept');
            });
            maskObject.on('complete', () => {
                if (!maskObject) return;
                maskIsComplete.value = true;
                maskRawInputValue.value = maskObject.rawInputValue;
                inputValue.value = maskObject.value;
                emit('maskComplete');
            });
            maskIsComplete.value = maskObject.masked.isComplete;
            maskRawInputValue.value = maskObject.rawInputValue;

            if (props.maskUnlazyOnFocus) {
                inputRef.value.addEventListener(
                    'focus',
                    function () {
                        if (!maskObject) return;
                        maskObject.updateOptions({ lazy: false });
                    },
                    true,
                );
                inputRef.value.addEventListener(
                    'blur',
                    function () {
                        if (!maskObject) return;
                        maskObject.updateOptions({ lazy: true });
                    },
                    true,
                );
            }
        }
    }
});

watch(vModel, (newValue) => {
    if (skipVModelUpd) return;
    if (maskObject) {
        maskObject.value = newValue;
    } else {
        inputValue.value = newValue.toString();
    }
});

let skipVModelUpd = false;

watch(inputValue, (newValue) => {
    skipVModelUpd = true;
    vModel.value = newValue.toString();
    nextTick(() => {
        skipVModelUpd = false;
    });
});

const onBlur = () => {
    isFocused.value = false;
    if (props.readValueFromVModelOnBlur) {
        inputValue.value = vModel.value;
    }
};

onUnmounted(() => {
    if (maskObject) {
        maskObject.destroy();
    }
});
</script>

<template>
    <div :class="[$style.input, required ? $style.required : null]">
        <template v-if="mask">
            <input
                ref="inputRef"
                :value="inputValue.toString()"
                :type="!type ? 'text' : type"
                :name="name"
                :placeholder="placeholder"
                :class="[isError || (!isFocused && maskRawInputValue.length > 0 && maskIsComplete === false) ? 'ui_red_border' : false]"
                @focus="isFocused = true"
                @blur="onBlur"
            />
        </template>
        <template v-else>
            <input
                ref="inputRef"
                v-model="inputValue"
                :type="!type ? 'text' : type"
                :name="name"
                :min="min"
                :max="max"
                :step="step"
                :placeholder="placeholder"
                :class="[isError ? 'ui_red_border' : false]"
                @focus="isFocused = true"
                @blur="onBlur"
            />
        </template>
        <span v-if="required && typeof inputValue === 'string' && inputValue.length === 0">*</span>
    </div>
</template>

<style lang="less" module>
@import '@styles/includes';

.input {
    position: relative;
    font-size: 0;

    > input {
        background: var(--ui-bg-color);
        height: 50px;
        width: 100%;
        border: 1px solid var(--ui-border-color);
        border-radius: 5px;
        padding: 0 15px;
        box-sizing: border-box;
        font-size: 16px;
        color: var(--ui-text-color);

        &::placeholder {
            color: #b8babf;
            opacity: 1;
        }

        &:focus-visible {
            box-shadow: 0px 0px 3px 2px var(--ui-focus-shadow);
        }
    }

    &.required {
        > span {
            display: block;
            position: absolute;
            font-size: 16px;
            color: var(--color-1);
            top: 0;
            left: 0;
            height: 100%;
            padding: 8px 0 0 5px;
        }
    }

    .width-size-sm-less({
        > input {
            height:40px;
            border-radius: 5px;
        }
    });
}
</style>
