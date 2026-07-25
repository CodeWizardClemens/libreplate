import { useRef } from "react";

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
  const dateInputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    if (dateInputRef.current) {
      // Trigger the native date picker
      if (typeof dateInputRef.current.showPicker === "function") {
        dateInputRef.current.showPicker();
      } else {
        // Fallback for older browsers
        dateInputRef.current.click();
      }
    }
  };

  const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChangeDate(event.target.value);
  };

  const formattedButtonLabel = new Date(selectedDate).toLocaleDateString(
    undefined,
    {
      month: "long",
      day: "numeric",
      year: "numeric",
    }
  );

  return (
    <div className="d-flex justify-content-center mb-3">
      <div className="d-flex flex-wrap justify-content-center align-items-center gap-2">

        <button
          onClick={onPrevious}
          className="btn btn-outline-secondary d-flex align-items-center gap-1 flex-shrink-0"
          aria-label="Previous day"
        >
          <i className="bi bi-chevron-left" />
          <span className="d-none d-sm-inline">Previous</span>
        </button>

        {/* Date picker button */}
        <div className="position-relative flex-shrink-0" style={{ minWidth: "170px" }}>
          {/* Hidden native input - positioned absolutely but below the button */}
          <input
            ref={dateInputRef}
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            style={{
              position: "absolute",
              inset: 0,
              opacity: 0,
              zIndex: -1,
              cursor: "pointer",
            }}
            tabIndex={-1}
          />
          
          <button
            onClick={handleButtonClick}
            type="button"
            className="btn btn-outline-primary d-flex align-items-center justify-content-center gap-2 w-100 position-relative"
            style={{ zIndex: 0 }}
          >
            <i className="bi bi-calendar3" />
            <span>{formattedButtonLabel}</span>
          </button>
        </div>

        <button
          onClick={onToday}
          className="btn btn-primary flex-shrink-0"
          disabled={selectedDate === todayString}
        >
          Today
        </button>

        <button
          onClick={onNext}
          className="btn btn-outline-secondary d-flex align-items-center gap-1 flex-shrink-0"
          aria-label="Next day"
        >
          <span className="d-none d-sm-inline">Next</span>
          <i className="bi bi-chevron-right" />
        </button>
      </div>
    </div>
  );
}