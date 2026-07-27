import { createBrowserRouter, Navigate, redirect } from "react-router-dom";

import AppLayout from "./AppLayout";

import {
  accountsMeRetrieve,
} from "@/api/generated/sdk.gen";

import LoginPage from "../features/auth/LoginPage";
import RecipesPage from "../features/recipes/RecipePage";
import RecipeEditPage from "../features/recipes/RecipeEditPage";
import FoodEditPage from "../features/foods/FoodEditPage";
import FoodsPage from "../features/foods/FoodsPage";
import DiaryPage from "../features/diary/DiaryPage";

function Placeholder({ title }: { title: string }) {
  return (
    <>
      <h1>{title}</h1>
      <p>Coming soon.</p>
    </>
  );
}

async function authLoader() {
  try {
    const response = await accountsMeRetrieve();

    return response.data;
  } catch {
    throw redirect("/login");
  }
}

const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },

  {
    loader: authLoader,
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/diary" replace />,
      },

      {
        path: "diary",
        element: <DiaryPage />,
        handle: {
          title: "Diary",
        },
      },

      {
        path: "groceries",
        element: <Placeholder title="Groceries" />,
        handle: {
          title: "Groceries",
        },
      },

      {
        path: "recipes",
        element: <RecipesPage />,
        handle: {
          title: "My Recipes",
        },
      },

      {
        path: "recipes/:id/edit",
        element: <RecipeEditPage />,
        handle: {
          title: "Edit Recipe",
        },
      },

      {
        path: "foods/:id/edit",
        element: <FoodEditPage />,
        handle: {
          title: "Edit Food",
        },
      },

      {
        path: "foods",
        element: <FoodsPage />,
        handle: {
          title: "Foods",
        },
      },

      {
        path: "meal-plans",
        element: <Placeholder title="Meal Plans" />,
        handle: {
          title: "Meal Plans",
        },
      },

      {
        path: "statistics",
        element: <Placeholder title="Statistics" />,
        handle: {
          title: "Statistics",
        },
      },

      {
        path: "goals",
        element: <Placeholder title="Goals" />,
        handle: {
          title: "Goals",
        },
      },

      {
        path: "settings",
        element: <Placeholder title="Settings" />,
        handle: {
          title: "Settings",
        },
      },

      {
        path: "account",
        element: <Placeholder title="Account" />,
        handle: {
          title: "Account",
        },
      },
    ],
  },
]);

export default router;