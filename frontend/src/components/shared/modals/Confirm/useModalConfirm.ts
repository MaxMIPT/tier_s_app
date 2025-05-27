import { useModal, type ModalSlot } from 'vue-final-modal';
import SharedModalsConfirm from './Confirm.vue';

interface IProps {
    slot: ModalSlot;
    title?: string;
    onConfirm?: () => void;
}

export const useModalConfirm = (props: IProps) => {
    props = { title: 'Внимание!', ...props };

    const modal = useModal({
        component: SharedModalsConfirm,
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
