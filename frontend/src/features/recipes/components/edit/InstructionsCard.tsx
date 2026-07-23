import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

import type { Recipe } from "../../types";
import { useUpdateRecipe } from "../../api";

type Props = {
  recipe: Recipe;
};

export default function InstructionsCard({ recipe }: Props) {
  const [editing, setEditing] = useState(false);
  const [instructions, setInstructions] = useState(recipe.instructions);

  const cardRef = useRef<HTMLDivElement>(null);

  const updateRecipe = useUpdateRecipe();

  useEffect(() => {
    if (editing) {
      cardRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [editing]);

  function saveInstructions() {
    updateRecipe.mutate(
      {
        id: recipe.id,
        data: {
          instructions,
        },
      },
      {
        onSuccess() {
          setEditing(false);
        },
      },
    );
  }

  return (
    <div className="card mb-4" ref={cardRef}>
      <div className="card-header d-flex justify-content-between align-items-center">
        <div className="d-flex align-items-center gap-2">
          <h5 className="mb-0">Instructions</h5>

          <i
            className="bi bi-info-circle text-info"
            role="button"
            title="Instructions support Markdown formatting. Use **bold**, # headings, and - lists."
          />
        </div>

        <div className="d-flex align-items-center gap-2">
          {editing && (
            <button
              className="btn btn-primary btn-sm"
              onClick={saveInstructions}
              disabled={updateRecipe.isPending}
            >
              {updateRecipe.isPending ? "Saving..." : "Save"}
            </button>
          )}

          <button
            className="btn btn-link"
            onClick={() => setEditing((value) => !value)}
          >
            <i className={`bi ${editing ? "bi-x" : "bi-pencil"}`} />
          </button>
        </div>
      </div>

      <div className="card-body">
        {editing ? (
          <textarea
            className="form-control"
            rows={10}
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
          />
        ) : (
          <ReactMarkdown>{instructions}</ReactMarkdown>
        )}
      </div>
    </div>
  );
}