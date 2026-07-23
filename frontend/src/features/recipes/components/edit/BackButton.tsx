type Props = {
  onClick: () => void;
};

export default function BackButton({ onClick }: Props) {
  return (
    <div className="mb-3">
      <button
        className="btn btn-outline-secondary"
        onClick={onClick}
      >
        <i className="bi bi-arrow-left me-2" />
        Back to recipes
      </button>
    </div>
  );
}