import { useState } from "react";

import type { Food } from "@/types/FoodTypes";
import { useEditableFieldKeyboard } from "@/hooks/useEditableFieldKeyboard";

interface Props {
  food: Food;
  update: (data: { name?: string; description?: string }) => void;
  editingName: boolean;
  setEditingName: (value: boolean) => void;
  editingDescription: boolean;
  setEditingDescription: (value: boolean) => void;
}

type Field = "name" | "description";

export default function FoodCardHeader({
  food,
  update,
  editingName,
  setEditingName,
  editingDescription,
  setEditingDescription,
}: Props) {
  const [values, setValues] = useState({
    name: food.name,
    description: food.description ?? "",
  });

  const [hoveredField, setHoveredField] = useState<Field | null>(null);

  const currentValue = (field: Field) =>
    field === "name" ? food.name : (food.description ?? "");

  const edit = (field: Field) => {
    setValues((v) => ({
      ...v,
      [field]: currentValue(field),
    }));

    field === "name" ? setEditingName(true) : setEditingDescription(true);
  };

  const save = (field: Field) => {
    update({
      [field]: values[field],
    });

    field === "name" ? setEditingName(false) : setEditingDescription(false);
  };

  const cancel = (field: Field) => {
    setValues((v) => ({
      ...v,
      [field]: currentValue(field),
    }));

    field === "name" ? setEditingName(false) : setEditingDescription(false);
  };

  const nameKeyDown = useEditableFieldKeyboard({
    save: () => save("name"),
    cancel: () => cancel("name"),
  });

  const descriptionKeyDown = useEditableFieldKeyboard({
    save: () => save("description"),
    cancel: () => cancel("description"),
  });

  const stopCardClick = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  const updateValue = (field: Field, value: string) => {
    setValues((v) => ({
      ...v,
      [field]: value,
    }));
  };

  const renderEditButton = (field: Field, editing: boolean) =>
    !editing &&
    hoveredField === field && (
      <button
        type="button"
        className="btn btn-sm btn-link p-0"
        title={`Edit ${field}`}
        onClick={(e) => {
          stopCardClick(e);
          edit(field);
        }}
      >
        <i className="bi bi-pencil" />
      </button>
    );

  const renderField = (field: Field, editing: boolean) =>
    editing ? (
      field === "name" ? (
        <input
          className="form-control"
          style={{
            minWidth: "280px",
          }}
          value={values[field]}
          autoFocus
          onClick={stopCardClick}
          onChange={(e) => updateValue(field, e.target.value)}
          onKeyDown={nameKeyDown}
          onBlur={() => save(field)}
        />
      ) : (
        <textarea
          className="form-control"
          style={{
            minWidth: "320px",
            resize: "vertical",
          }}
          value={values[field]}
          autoFocus
          rows={1}
          onClick={stopCardClick}
          onChange={(e) => updateValue(field, e.target.value)}
          onKeyDown={descriptionKeyDown}
          onBlur={() => save(field)}
        />
      )
    ) : field === "name" ? (
      <h5 className="card-title mb-0">{food.name}</h5>
    ) : (
      <p className="card-text mb-0 text-muted">
        {food.description || "No description"}
      </p>
    );

  const renderEditableRow = (field: Field, editing: boolean) => (
    <div
      className="d-flex align-items-center gap-2 w-100"
      onMouseEnter={() => setHoveredField(field)}
      onMouseLeave={() => setHoveredField(null)}
      onClick={(e) => {
        stopCardClick(e);

        if (!editing) {
          edit(field);
        }
      }}
      style={{
        cursor: editing ? "default" : "pointer",
      }}
    >
      {renderField(field, editing)}
      {renderEditButton(field, editing)}
    </div>
  );

  return (
    <>
      {renderEditableRow("name", editingName)}

      <div className="mt-1 w-100">
        {renderEditableRow("description", editingDescription)}
      </div>
    </>
  );
}
