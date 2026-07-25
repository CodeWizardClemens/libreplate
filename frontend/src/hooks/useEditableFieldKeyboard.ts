import type React from "react";

interface Options {
  save: () => void;
  cancel: () => void;
  allowEnter?: boolean;
}

export function useEditableFieldKeyboard({
  save,
  cancel,
  allowEnter = true,
}: Options) {
  return (
    event: React.KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    if (event.key === "Escape") {
      event.preventDefault();
      cancel();
      return;
    }

    if (
      event.key === "Enter" &&
      allowEnter &&
      !(event.currentTarget instanceof HTMLTextAreaElement && event.shiftKey)
    ) {
      event.preventDefault();
      save();
    }
  };
}