import type { THEME } from './types';

const LAST_APP_THEME_COOKIE_KEY = 'last_app_theme';
const LAST_APP_THEME_COOKIE_MAXAGE = () => 3600 * 24 * 365;
const MANUAL_APP_THEME_COOKIE_KEY = 'session_app_theme';

const THEMES: THEME[] = ['dark', 'light'];

export function getCurrentTheme(): THEME {
    const lastCookieAppTheme = useCookie(LAST_APP_THEME_COOKIE_KEY, { maxAge: LAST_APP_THEME_COOKIE_MAXAGE() });
    const manualCookieAppTheme = useCookie(MANUAL_APP_THEME_COOKIE_KEY);

    let theme: THEME = 'light';

    if (THEMES.find((t) => t == manualCookieAppTheme.value)) {
        theme = manualCookieAppTheme.value as THEME;
    } else if (THEMES.find((t) => t == lastCookieAppTheme.value)) {
        theme = lastCookieAppTheme.value as THEME;
    }

    if (import.meta.server) {
        return theme;
    }

    if (THEMES.find((t) => t == manualCookieAppTheme.value) === undefined) {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            theme = 'dark';
        } else {
            theme = 'light';
        }
    }

    return theme;
}

export function setTheme(theme: THEME) {
    if (import.meta.server) {
        return;
    }

    const lastCookieAppTheme = useCookie(LAST_APP_THEME_COOKIE_KEY, { maxAge: LAST_APP_THEME_COOKIE_MAXAGE() });
    lastCookieAppTheme.value = theme;

    document.body.classList.add('no_transition');
    document.documentElement.setAttribute('data-app-theme', theme);

    setTimeout(() => {
        document.body.classList.remove('no_transition');
    }, 500);
}

export function saveManualThemeValue(theme: THEME) {
    if (import.meta.server) {
        return;
    }

    const manualCookieAppTheme = useCookie(MANUAL_APP_THEME_COOKIE_KEY);
    manualCookieAppTheme.value = theme;
}
