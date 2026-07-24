import {
    createBrowserRouter,
    Navigate,
} from "react-router-dom";

import AppLayout from "./AppLayout";

import LoginPage from "../features/auth/pages/LoginPage";
import GroceriesPage from "../features/groceries/pages/GroceriesPage";
import RecipesPage from "../features/recipes/RecipePage";
import RecipeEditPage from "../features/recipes/RecipeEditPage";
import FoodsPage from "../features/foods/FoodsPage";


function Placeholder({ title }: { title: string }) {
    return (
        <>
            <h1>{title}</h1>
            <p>Coming soon.</p>
        </>
    );
}


const router = createBrowserRouter([
    {
        path: "/login",
        element: <LoginPage />,
    },

    {
        element: <AppLayout />,
        children: [
            {
                index: true,
                element: <Navigate to="/groceries" replace />,
            },

            {
                path: "groceries",
                element: <GroceriesPage />,
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