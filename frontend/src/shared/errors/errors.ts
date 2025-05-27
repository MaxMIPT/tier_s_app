import { FetchError } from 'ofetch';

export class StandartErrorList extends Error {
    details: string[] = [];
    code: number = 400;
    constructor(details: string[], code: number = 400, text: string = 'bad request to api') {
        super(text);
        this.code = code;
        this.details = details;
    }
}

export function tryToThrowApiErrors(e: unknown) {
    if (e instanceof FetchError && e.statusCode) {
        if (e.statusCode === 429) {
            return new StandartErrorList(['Вы отправляете слишком много запросов, попробуйте повторить через 2 минуты'], e.statusCode);
        } else if (e.statusCode >= 400 && e.statusCode < 500 && e.data && typeof e.data.details == 'object') {
            return new StandartErrorList(e.data.details, e.statusCode);
        } else if (e.statusCode >= 400 && e.statusCode < 500 && e.data && typeof e.data.error == 'string') {
            return new StandartErrorList([e.data.error], e.statusCode);
        }
        return new StandartErrorList(['Произошла неизвестная ошибка, попробуйте повторить запрос позже'], e.statusCode);
    }
    return e;
}
