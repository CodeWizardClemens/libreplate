import type { Recipe } from "../types";

interface Props {
    recipe: Recipe;
    onCopy: () => void;
    onDelete?: (id: number) => void;
    onToggleFavorite?: (id: number) => void;
    onTogglePinned?: (id: number) => void;
}

export default function RecipeCardActions({
    recipe,
    onCopy,
    onDelete,
    onToggleFavorite,
    onTogglePinned,
}: Props) {
    const handleDelete = () => {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${recipe.name}"? This cannot be undone.`
        );

        if (confirmed) {
            onDelete?.(recipe.id);
        }
    };

    const actions = (
        <>
            <button
                className="btn btn-outline-secondary"
                onClick={() => onTogglePinned?.(recipe.id)}
                title="Pin"
            >
                <i className={recipe.is_pinned ? "bi bi-pin-fill" : "bi bi-pin"} />
            </button>

            <button
                className="btn btn-outline-warning"
                onClick={() => onToggleFavorite?.(recipe.id)}
                title="Favorite"
            >
                <i
                    className={
                        recipe.is_favorite
                            ? "bi bi-star-fill"
                            : "bi bi-star"
                    }
                />
            </button>

            <button
                className="btn btn-outline-primary"
                onClick={onCopy}
                title="Copy"
            >
                <i className="bi bi-copy" />
            </button>

            <button
                className="btn btn-outline-danger"
                onClick={handleDelete}
                title="Delete"
            >
                <i className="bi bi-trash" />
            </button>
        </>
    );

    return (
        <>
            {/* Desktop */}
            <div className="col-12 col-md-auto d-none d-md-flex gap-2 order-3">
                {actions}
            </div>

            {/* Mobile */}
            <div className="d-flex d-md-none justify-content-end gap-2 mt-3 order-3 flex-wrap">
                {actions}
            </div>
        </>
    );
}