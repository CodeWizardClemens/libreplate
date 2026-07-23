import { useState } from "react";
import type { Recipe } from "../types";
import { useEditableFieldKeyboard } from "../../../../hooks/useEditableFieldKeyboard";

interface Props {
  recipe: Recipe;
  update: (data: { name?: string; summary?: string }) => void;
  editingName: boolean;
  setEditingName: (value: boolean) => void;
  editingSummary: boolean;
  setEditingSummary: (value: boolean) => void;
}

type Field = "name" | "summary";

export default function RecipeCardHeader({
  recipe,
  update,
  editingName,
  setEditingName,
  editingSummary,
  setEditingSummary,
}: Props) {
  const [values, setValues] = useState({
    name: recipe.name,
    summary: recipe.summary,
  });

  const [hoveredField, setHoveredField] = useState<Field | null>(null);

  const edit = (field: Field) => {
    setValues((v) => ({
      ...v,
      [field]: recipe[field],
    }));

    field === "name"
      ? setEditingName(true)
      : setEditingSummary(true);
  };

  const save = (field: Field) => {
    update({
      [field]: values[field],
    });

    field === "name"
      ? setEditingName(false)
      : setEditingSummary(false);
  };

  const cancel = (field: Field) => {
    setValues((v) => ({
      ...v,
      [field]: recipe[field],
    }));

    field === "name"
      ? setEditingName(false)
      : setEditingSummary(false);
  };

  const nameKeyDown = useEditableFieldKeyboard({
    save: () => save("name"),
    cancel: () => cancel("name"),
  });

  const summaryKeyDown = useEditableFieldKeyboard({
    save: () => save("summary"),
    cancel: () => cancel("summary"),
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

  const renderEditButton = (
    field: Field,
    editing: boolean
  ) =>
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

  const renderField = (
    field: Field,
    editing: boolean
  ) =>
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
          onChange={(e) =>
            updateValue(field, e.target.value)
          }
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
          onChange={(e) =>
            updateValue(field, e.target.value)
          }
          onKeyDown={summaryKeyDown}
          onBlur={() => save(field)}
        />
      )
    ) : field === "name" ? (
      <h5 className="card-title mb-0">
        {recipe[field]}
      </h5>
    ) : (
      <p className="card-text mb-0">
        {recipe[field]}
      </p>
    );

  const renderEditableRow = (
    field: Field,
    editing: boolean
  ) => (
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
        {renderEditableRow("summary", editingSummary)}
      </div>
    </>
  );
}