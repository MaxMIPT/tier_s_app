import { useModal } from 'vue-final-modal';
import SharedModalsErrorsList from './ErrorsList.vue';

interface IProps {
    errors: MaybeRef<string[]>;
    title?: string;
    onConfirm?: () => void;
}

export const useModalErrorsList = (props: IProps) => {
    props = { title: 'Возникли ошибки!', ...props };

    const modal = useModal({
        component: SharedModalsErrorsList,
        attrs: {
            title: props.title,
            errors: props.errors,
            modalObj: () => modal,
            onConfirm: () => {
                props.onConfirm?.();
            },
        },
    });

    return modal;
};
