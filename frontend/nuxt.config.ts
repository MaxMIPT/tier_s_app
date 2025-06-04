// https://nuxt.com/docs/api/configuration/nuxt-config
import type { NuxtConfig } from 'nuxt/schema';
import type { ConfigLayerMeta, InputConfig } from 'c12';

const config: InputConfig<NuxtConfig, ConfigLayerMeta> = {
    compatibilityDate: '2024-11-01',
    devtools: { enabled: false },
    $production: {
        nitro: {
            compressPublicAssets: true,
        },
    },
    devServer: {
        host: '0.0.0.0',
    },
    ssr: false,
    srcDir: 'src',
    alias: {
        '@styles': '/assets/styles',
    },
    dir: {
        pages: 'routes',
    },
    components: [
        {
            path: '~/components/shared',
            extensions: ['.vue'],
            prefix: 'Shared',
        },
        {
            path: '~/components/features',
            extensions: ['.vue'],
            prefix: 'Feature',
        },
        {
            path: '~/components/entities',
            extensions: ['.vue'],
            prefix: 'Entity',
        },
        {
            path: '~/components/widgets',
            extensions: ['.vue'],
            prefix: 'Widget',
        },
        {
            path: '~/components/pages',
            extensions: ['.vue'],
            prefix: 'Page',
        },
    ],
    css: ['@/assets/styles/index.less', '@/assets/styles/nuxt-ui.css'],
    modules: [
        '@nuxt/eslint',
        '@nuxtjs/google-fonts',
        '@hypernym/nuxt-anime',
        '@vue-final-modal/nuxt',
        '@pinia/nuxt',
        '@vueuse/nuxt',
        '@nuxt/ui',
    ],
    vite: {
        build: {
            assetsInlineLimit: 0,
            target: ['es2015'],
        },
    },
    experimental: {
        // @ts-ignore
        inlineSSRStyles: false,
    },
    anime: {
        composables: true,
    },
    app: {
        baseURL: '/',
        head: {
            viewport: 'width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no',
        },
        pageTransition: {
            name: 'page',
            mode: 'out-in',
        },
        layoutTransition: {
            name: 'page',
            mode: 'out-in',
        },
    },
    runtimeConfig: {
        public: {
            apiBase: '',
            apiWs: '',
            apiWsProtocol: '',
            storageBase: '',
        },
    },
    googleFonts: {
        families: {
            Inter: [400, 500, 600, 700],
        },
    },
};

const defaultConfig = defineNuxtConfig(config);

export default defaultConfig;
