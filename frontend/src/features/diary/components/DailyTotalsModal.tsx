import Modal from "@/components/ui/Modal";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  totals: {
    energy: number;
    protein: number;
    fat: number;
    carbs: number;
  };
};

export default function DailyTotalsModal({ isOpen, onClose, totals }: Props) {
  return (
    <Modal isOpen={isOpen} title="Daily Total" onClose={onClose}>
      {/* TODO query nutrients, don't hardcode them! */}
      <div>
        <div className="d-flex justify-content-between py-2">
          <span>Energy</span>
          <span>{totals.energy.toFixed(0)} kcal</span>
        </div>

        <div className="d-flex justify-content-between py-2">
          <span>Protein</span>
          <span>{totals.protein.toFixed(0)} g</span>
        </div>

        <div className="d-flex justify-content-between py-2">
          <span>Fat</span>
          <span>{totals.fat.toFixed(0)} g</span>
        </div>

        <div className="d-flex justify-content-between py-2">
          <span>Carbohydrates</span>
          <span>{totals.carbs.toFixed(0)} g</span>
        </div>
      </div>
    </Modal>
  );
}
