// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt({
    files: ["**/*.ts", "**/*.vue"],
    rules: {
        "no-unused-vars": "warn",
        "@typescript-eslint/no-unused-vars": "warn",
        "vue/no-multiple-template-root": "off",
        "vue/multi-word-component-names": "off",
        "@typescript-eslint/ban-ts-comment": "off",
        "@typescript-eslint/no-explicit-any": "warn",
        "vue/html-self-closing": "off",
        "@typescript-eslint/unified-signatures": "off",
    },
});
