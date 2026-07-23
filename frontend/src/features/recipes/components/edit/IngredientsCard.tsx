type Props = {
  ingredients: any;
};

export default function IngredientsCard({
  ingredients,
}: Props) {
  const dummyIngredients = [
    {
      food_name: "Chicken",
      servings: 2,
      size: "150g",
      kcal: 330,
      protein: "62g",
      carbs: "0g",
    },
    {
      food_name: "Rice",
      servings: 3,
      size: "100g",
      kcal: 360,
      protein: "7g",
      carbs: "78g",
    },
  ];

  return (
    <div className="card">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h5 className="mb-0">
          Ingredients
        </h5>

        <button className="btn btn-outline-primary btn-sm">
          <i className="bi bi-plus" /> Food
        </button>
      </div>

      <div className="card-body p-0">
        <table className="table mb-0">
          <thead>
            <tr>
              <th>Food</th>
              <th>Serving</th>
              <th>Size</th>
              <th>kcal</th>
              <th>P</th>
              <th>C</th>
            </tr>
          </thead>

          <tbody>
            {dummyIngredients.map((item) => (
              <tr key={item.food_name}>
                <td>{item.food_name}</td>
                <td>{item.servings}</td>
                <td>{item.size}</td>
                <td>{item.kcal}</td>
                <td>{item.protein}</td>
                <td>{item.carbs}</td>
              </tr>
            ))}

            <tr className="fw-bold">
              <td>Total</td>
              <td />
              <td />
              <td>690</td>
              <td>69g</td>
              <td>78g</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}