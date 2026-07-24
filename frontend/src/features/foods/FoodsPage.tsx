import { useFoods } from "./api";


export default function FoodsPage() {
  const {
    data: foods,
    isLoading,
    isError,
  } = useFoods();


  if (isLoading) {
    return <div>Loading foods...</div>;
  }


  if (isError) {
    return <div>Failed to load foods.</div>;
  }


  return (
    <div>
      <h1>Foods</h1>

      {foods?.length === 0 ? (
        <p>No foods found.</p>
      ) : (
        <ul>
          {foods?.map((food) => (
            <li key={food.id}>
              <div>
                <strong>{food.name}</strong>

                {food.brand && (
                  <span> ({food.brand})</span>
                )}
              </div>

              <div>
                Serving: {food.serving ?? "-"} {food.unit}
              </div>

              {food.description && (
                <p>{food.description}</p>
              )}

              {food.nutrients.length > 0 && (
                <ul>
                  {food.nutrients.map((nutrient) => (
                    <li
                      key={`${food.id}-${nutrient.nutrient_name}`}
                    >
                      {nutrient.nutrient_name}:{" "}
                      {nutrient.amount}{" "}
                      {nutrient.nutrient_unit}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}