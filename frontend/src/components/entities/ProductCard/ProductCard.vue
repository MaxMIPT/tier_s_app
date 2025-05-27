<script setup lang="ts">
import { coolNumber } from '~/shared/helpers/functions';
import type { ProductCardProps } from './model/types/types';
import { addProductToCart } from '~/domain/shop';

const props = defineProps<ProductCardProps>();
</script>

<template>
    <div :class="$style.wrapper">
        <NuxtLink
            :to="`/product-${props.product.id}`"
            :class="$style.img"
        >
            <img
                v-if="props.product.image_preview"
                :src="props.product.image_preview"
                :alt="props.product.name"
                :title="props.product.name"
                loading="lazy"
            />
            <span></span>
        </NuxtLink>
        <div :class="$style.price">
            <div :class="$style.value">{{ coolNumber(props.product.price) }} ₽</div>
            <div :class="$style.cart">
                <template v-if="props.product.stock_available">
                    <button
                        :class="$style.add_to_cart"
                        title="Добавить в корзину"
                        @click="addProductToCart(props.product.id)"
                    ></button>
                </template>
                <template v-else>
                    <span
                        :class="$style.add_to_cart"
                        title="Нет в наличии"
                    ></span>
                </template>
            </div>
        </div>
        <NuxtLink
            :to="`/product-${props.product.id}`"
            :class="$style.name"
        >
            {{ props.product.name }}
        </NuxtLink>
    </div>
</template>

<style lang="less" module>
@import '@styles/includes';

.wrapper {
    width: 100%;
}

.img {
    display: block;
    position: relative;
    background-color: var(--ui-bg-color);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.01);
    transition: box-shadow 0.3s ease;

    > img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    > span {
        display: block;
        padding-top: 100%;
    }

    .hover({
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    });
}

.name {
    overflow: hidden;
    width: 100%;
    word-break: break-word;
    display: block;
    margin-top: 15px;
    font-family: 'Strong';
    text-decoration: underline;
    text-decoration-thickness: 1px;
    font-size: 20px;
    color: var(--font-color-3);

    .width-size-sm-less({
        font-size: 16px;
    });

    .hover({
        text-decoration: none;
    });
}

.add_to_cart {
    display: block;
    width: 30px;
    height: 30px;
    border-radius: 5px;
    position: relative;
    transition: background-color 0.3s ease;

    .width-size-sm-less({
        width: 24px;
        height: 24px;
    });

    &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: var(--stable-white-color);
        mask: url('@/assets/icons/basket.svg') no-repeat center center;
        mask-size: 22px auto;

        .width-size-sm-less({
            mask-size: 18px auto;
        });
    }
}

.price {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;

    > .value {
        font-size: 16px;
        font-weight: 600;
        color: var(--font-color-3);
    }

    > .cart {
        flex-shrink: 0;

        > button {
            background-color: var(--color-1);

            .hover({
                background-color: var(--color-1-hover);
            });
        }

        > span {
            background-color: var(--color-2);
        }
    }
}
</style>
