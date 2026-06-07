import { toast } from "vue-sonner";

const DEFAULT_DURATION = 3600;

export function notifySuccess(message, description) {
  toast.success(message, {
    description,
    duration: DEFAULT_DURATION,
  });
}

export function notifyError(message, description) {
  toast.error(message, {
    description,
    duration: 5200,
  });
}

export function notifyInfo(message, description) {
  toast(message, {
    description,
    duration: DEFAULT_DURATION,
  });
}

