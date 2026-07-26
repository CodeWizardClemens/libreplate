type Props = {
  isOpen: boolean;
  onClose: () => void;
  onFood: () => void;
  onRecipe: () => void;
};

export default function AddToMealModal({
  isOpen,
  onClose,
  onFood,
  onRecipe,
}: Props) {
  if (!isOpen) return null;

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1050,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "white",
          padding: "20px",
          width: "420px",
          borderRadius: "8px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
          }}
        >
          <h2 style={{ margin: 0 }}>Add to meal</h2>

          <button
            type="button"
            onClick={onClose}
            style={{
              border: "none",
              background: "transparent",
              fontSize: "1.5rem",
              cursor: "pointer",
              lineHeight: 1,
            }}
          >
            ×
          </button>
        </div>

        <div
          style={{
            display: "grid",
            gap: "12px",
          }}
        >
          <button className="btn btn-outline-primary" onClick={onRecipe}>
            <i className="bi bi-journal-text me-2" />
            Search Recipes
          </button>

          <button className="btn btn-outline-primary" onClick={onFood}>
            <i className="bi bi-cake2 me-2" />
            Search Foods
          </button>
        </div>
      </div>
    </div>
  );
}
