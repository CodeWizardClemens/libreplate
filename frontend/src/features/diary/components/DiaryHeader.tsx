function displayDate(date: string) {
  return new Date(date).toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

type Props = {
  selectedDate: string;
  todayString: string;
  onChangeDate: (date: string) => void;
  onPrevious: () => void;
  onNext: () => void;
  onToday: () => void;
};

export default function DiaryHeader({
  selectedDate,
  todayString,
  onChangeDate,
  onPrevious,
  onNext,
  onToday,
}: Props) {
  return (
    <div className="d-flex justify-content-center align-items-center mb-4 w-100">
      <div className="d-flex align-items-center gap-3 flex-nowrap">
        <button
          onClick={onPrevious}
          className="btn btn-outline-secondary px-3 text-nowrap d-flex align-items-center gap-2"
          aria-label="Previous day"
        >
          <i className="bi bi-chevron-left" />
          Previous
        </button>

        <input
          type="date"
          value={selectedDate}
          onChange={(event) => onChangeDate(event.target.value)}
          className="form-control"
          style={{ width: "190px" }}
        />

        <button
          onClick={onToday}
          className="btn btn-primary px-4 text-nowrap"
          disabled={selectedDate === todayString}
        >
          Today
        </button>

        <button
          onClick={onNext}
          className="btn btn-outline-secondary px-3 text-nowrap d-flex align-items-center gap-2"
          aria-label="Next day"
        >
          Next
          <i className="bi bi-chevron-right" />
        </button>
      </div>
    </div>
  );
}