import { useEffect, useRef, useState } from "react";

export function useInlineEdit<T extends object>(
  item: T,
  onSave: (field: keyof T, value: string) => void,
) {
  const [editing, setEditing] = useState<keyof T | null>(null);
  const [value, setValue] = useState("");

  const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

  useEffect(() => {
    if (editing) {
      inputRef.current?.focus();
    }
  }, [editing]);

  function edit(field: keyof T) {
    setEditing(field);
    setValue(String(item[field] ?? ""));
  }

  function cancel() {
    setEditing(null);
    setValue("");
  }

  function save() {
    if (!editing) return;

    const trimmed = value.trim();

    if (!trimmed || trimmed === String(item[editing] ?? "")) {
      cancel();
      return;
    }

    onSave(editing, trimmed);
    cancel();
  }

  function keyDown(event: React.KeyboardEvent) {
    if (event.key === "Enter") {
      event.preventDefault();
      save();
    }

    if (event.key === "Escape") {
      cancel();
    }
  }

  return {
    editing,
    value,
    setValue,
    inputRef,
    edit,
    save,
    cancel,
    keyDown,
  };
}