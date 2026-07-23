import type { RecipeTag } from "../../types";

interface Props {
  tags: RecipeTag[];
  selectedTags: number[];
  onChange: (tags: number[]) => void;
}

export default function TagSelector({ tags, selectedTags, onChange }: Props) {
  function toggleTag(id: number) {
    if (selectedTags.includes(id)) {
      onChange(selectedTags.filter((tagId) => tagId !== id));
    } else {
      onChange([...selectedTags, id]);
    }
  }

  return (
    <div className="d-flex flex-wrap gap-3">
      {tags.map((tag) => {
        const isSelected = selectedTags.includes(tag.id);

        return (
          <button
            key={tag.id}
            type="button"
            onClick={() => toggleTag(tag.id)}
            className={`
              btn btn-link p-0 text-decoration-none
              position-relative
              ${isSelected ? "text-primary fw-semibold" : "text-body"}
            `}
            style={{
              border: "none",
              background: "transparent",
            }}
          >
            {tag.name}
            {isSelected && (
              <span
                className="position-absolute start-0 bottom-0 w-100 bg-primary"
                style={{ height: "2px" }}
              />
            )}
          </button>
        );
      })}
    </div>
  );
}