<script setup lang="ts"></script>

<template>
    <div>
        <div :id="$style.block_desc">
            <div :class="$style.title">speechRecovery</div>
            <div :class="$style.text">
                Приложение помогает людям с нарушенной речью снова быть услышанными. Оно распознаёт их звучащую речь, преобразует в текст и
                озвучивает через синтезатор, создавая понятную и уверенную коммуникацию. Это цифровой голос, который говорит вместо человека
                — понятно, чётко и с уважением.
            </div>
        </div>
        <div :id="$style.block_app">
            <WidgetRecoveryApp />
        </div>
    </div>
</template>

<style lang="less" module>
@import '@styles/includes';

#block_desc {
    .std-wrapper();

    > .title {
        font-size: 32px;
        text-align: center;
        font-family: 'Strong';
        color: var(--font-color-3);

        .width-size-sm-less({
            font-size:24px;
        });
    }

    > .text {
        margin-top: 35px;
        line-height: 1.5;
        font-size: 14px;
        text-align: justify;

        .width-size-sm-less({
            font-size:12px;
            margin-top: 20px;
        });
    }
}

#block_app {
    .std-wrapper(50px, 0, 40px, 0);
}
</style>
