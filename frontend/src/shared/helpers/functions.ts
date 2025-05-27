export function nextAnimFrame(f: () => void) {
    if (!window) {
        f();
        return;
    }
    const raf = window.requestAnimationFrame || (window as any).webkitRequestAnimationFrame || (window as any).msRequestAnimationFrame;
    if (raf) {
        raf(() => {
            raf(() => {
                f();
            });
        });
    } else {
        f();
    }
}

export function waitNextAnimFrame(): Promise<void> {
    return new Promise((resolve) => {
        nextAnimFrame(resolve);
    });
}

interface elementAnimateOptions {
    transition: string;
    properties: Record<string, string>;
}

export function elementAnimate(elem: HTMLElement, options: elementAnimateOptions) {
    return new Promise<() => void>((resolve) => {
        const clearProperties = () => {
            Object.keys(options.properties).forEach((k) => {
                elem.style.removeProperty(k);
            });
        };

        const endHandler = (e: TransitionEvent) => {
            if (e.target === elem) {
                elem.removeEventListener('transitionend', endHandler);
                elem.style.removeProperty('transition');
                resolve(clearProperties);
            }
        };
        if (elem) {
            elem.addEventListener('transitionend', endHandler);
            elem.style.setProperty('transition', options.transition, 'important');
            nextAnimFrame(() => {
                Object.entries(options.properties).forEach(([k, value]) => {
                    elem.style.setProperty(k, value);
                });
            });
        }
    });
}

export function windowScrollToBlock(v: string, offset: number | undefined = undefined, is_smooth = true) {
    const elem = document.getElementById(v);
    if (!elem) return;
    if (offset === undefined) offset = window.innerWidth < 576 ? 70 : 100;
    windowScrollToElem(elem, offset, is_smooth);
}

export function windowScrollToElem(elem: HTMLElement, offset: number | undefined = undefined, is_smooth = true) {
    if (offset === undefined) offset = window.innerWidth < 576 ? 70 : 100;
    const s = elem.getBoundingClientRect().top + scrollY - offset;
    if (is_smooth) {
        windowScrollTo(s);
    } else {
        window.scrollTo({ top: s });
    }
}

export function windowScrollTo(v: number) {
    window.scrollTo({ top: v, behavior: 'smooth' });
}

export function numberFormat(number: number | string, decimals?: number, decPoint?: string, thousandsSep?: string) {
    number = `${number}`.replace(/[^0-9+\-Ee.]/g, '');
    const n = !Number.isFinite(+number) ? 0 : +number;
    decimals = decimals || 0;
    const prec = !Number.isFinite(+decimals) ? 0 : Math.abs(decimals);
    const sep = typeof thousandsSep === 'undefined' ? ',' : thousandsSep;
    const dec = typeof decPoint === 'undefined' ? '.' : decPoint;
    const toFixedFix = (n: number, prec: number) => {
        const k = 10 ** prec;
        return `${(Math.round(n * k) / k).toFixed(prec)}`;
    };
    const s = (prec ? toFixedFix(n, prec) : `${Math.round(n)}`).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

export function coolNumber(v: number) {
    return numberFormat(v, v === parseInt(v.toString(10), 10) ? 0 : 2, ',', ' ');
}

export function declOfNum(number: number, titles: [string, string, string]): string {
    const cases = [2, 0, 1, 1, 1, 2];
    return titles[number % 100 > 4 && number % 100 < 20 ? 2 : cases[Math.min(number % 10, 5)]];
}
