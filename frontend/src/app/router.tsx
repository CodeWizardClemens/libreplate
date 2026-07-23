import {
    createBrowserRouter,
    Navigate,
} from "react-router-dom";

import AppLayout from "./AppLayout";

import LoginPage from "../features/auth/pages/LoginPage";
import GroceriesPage from "../features/groceries/pages/GroceriesPage";
import RecipesPage from "../features/recipes/RecipePage";

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
            },

            {
                path: "recipes",
                element: <RecipesPage />,
            },

            {
                path: "foods",
                element: <Placeholder title="Foods" />,
            },

            {
                path: "meal-plans",
                element: <Placeholder title="Meal Plans" />,
            },

            {
                path: "statistics",
                element: <Placeholder title="Statistics" />,
            },

            {
                path: "goals",
                element: <Placeholder title="Goals" />,
            },

            {
                path: "settings",
                element: <Placeholder title="Settings" />,
            },

            {
                path: "account",
                element: <Placeholder title="Account" />,
            },
        ],
    },
]);

export default router;