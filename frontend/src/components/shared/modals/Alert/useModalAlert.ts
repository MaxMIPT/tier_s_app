import { useModal, type ModalSlot } from 'vue-final-modal';
import SharedModalsAlert from './Alert.vue';

interface IProps {
    slot: ModalSlot;
    title?: string;
    onConfirm?: () => void;
}

export const useModalAlert = (props: IProps) => {
    props = { title: 'Внимание!', ...props };

    const modal = useModal({
        component: SharedModalsAlert,
        attrs: {
            title: props.title,
            modalObj: () => modal,
            onConfirm: () => {
                props.onConfirm?.();
            },
        },
        slots: {
            default: props.slot,
        },
    });

    return modal;
};
