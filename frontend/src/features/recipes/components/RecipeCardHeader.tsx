import { useRef, useState } from "react";
import type { Recipe } from "../types";

interface Props {
  recipe: Recipe;
  update: (data: { name?: string; summary?: string }) => void;
  editingName: boolean;
  setEditingName: (value: boolean) => void;
  editingSummary: boolean;
  setEditingSummary: (value: boolean) => void;
}

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

  const cancelled = useRef(false);

  const edit = (field: "name" | "summary") => {
    setValues((v) => ({
      ...v,
      [field]: recipe[field],
    }));

    field === "name" ? setEditingName(true) : setEditingSummary(true);
  };

  const save = (field: "name" | "summary") => {
    update({
      [field]: values[field],
    });

    field === "name" ? setEditingName(false) : setEditingSummary(false);
  };

  const cancel = (field: "name" | "summary") => {
    cancelled.current = true;

    setValues((v) => ({
      ...v,
      [field]: recipe[field],
    }));

    field === "name" ? setEditingName(false) : setEditingSummary(false);
  };

  const keyDown = (
    field: "name" | "summary",
    event: React.KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    if (event.key === "Escape") {
      event.preventDefault();
      cancel(field);
      return;
    }

    if (event.key === "Enter" && (field === "name" || !event.shiftKey)) {
      event.preventDefault();
      save(field);
    }
  };

  const handleBlur = (field: "name" | "summary") => {
    if (cancelled.current) {
      cancelled.current = false;
      return;
    }

    save(field);
  };

  const renderEditButton = (field: "name" | "summary", editing: boolean) =>
    !editing && (
      <button
        type="button"
        className="btn btn-sm btn-link p-0"
        title={`Edit ${field}`}
        onClick={() => edit(field)}
      >
        <i className="bi bi-pencil" />
      </button>
    );

  const renderField = (field: "name" | "summary", editing: boolean) =>
    editing ? (
      field === "name" ? (
        <input
          className="form-control form-control-sm"
          value={values[field]}
          autoFocus
          onChange={(e) =>
            setValues({
              ...values,
              [field]: e.target.value,
            })
          }
          onKeyDown={(e) => keyDown(field, e)}
          onBlur={() => handleBlur(field)}
        />
      ) : (
        <textarea
          className="form-control form-control-sm"
          value={values[field]}
          autoFocus
          rows={2}
          onChange={(e) =>
            setValues({
              ...values,
              [field]: e.target.value,
            })
          }
          onKeyDown={(e) => keyDown(field, e)}
          onBlur={() => handleBlur(field)}
        />
      )
    ) : field === "name" ? (
      <h5 className="card-title mb-2">{recipe[field]}</h5>
    ) : (
      <p className="card-text mb-3">{recipe[field]}</p>
    );

  return (
    <>
      <div className="d-flex align-items-center gap-2">
        {renderField("name", editingName)}
        {renderEditButton("name", editingName)}
      </div>

      <div className="d-flex align-items-start gap-2">
        {renderField("summary", editingSummary)}
        {renderEditButton("summary", editingSummary)}
      </div>
    </>
  );
}
