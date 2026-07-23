type Props = {
  recipe?: any;
};

export default function RecipeHeaderCard({ recipe }: Props) {
  return (
    <div className="mx-auto mb-3" style={{ maxWidth: "550px" }}>
      <div className="card">
        <div className="card-body d-flex align-items-center justify-content-center gap-4 py-2">
          <span>
            <i className="bi bi-people me-1" />
            <strong>0</strong>
          </span>

          <span>
            <i className="bi bi-stopwatch me-1" />
            <strong>Prep:</strong> 2m
          </span>

          <span>
            <i className="bi bi-stopwatch me-1" />
            <strong>Cooking:</strong> 2m
          </span>

          <span>
            <i className="bi bi-stopwatch me-1" />
            <strong>Total:</strong> 2m
          </span>
        </div>
      </div>
    </div>
  );
}