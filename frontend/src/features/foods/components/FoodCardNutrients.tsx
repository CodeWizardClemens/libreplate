import type { Food } from "@/api/generated";

interface Props {
  nutrients?: Food["nutrients"];
}

export default function EnergyNutrient({ nutrients }: Props) {
  const energy = nutrients?.find(
    (nutrient) => nutrient.nutrient_name.toLowerCase() === "energy",
  );

  return (
    <>
      {energy?.amount ?? 0}
      {/* TODO, kcals should not be hard coded! Implement unit in backend. */}
      {energy?.nutrient_unit ?? " kcals"}
    </>
  );
}
