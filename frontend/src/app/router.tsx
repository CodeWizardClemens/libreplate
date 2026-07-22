import {
    createBrowserRouter,
} from "react-router-dom";


import GroceriesPage from "../features/groceries/pages/GroceriesPage";
import LoginPage from "../features/auth/pages/LoginPage";


const router =
    createBrowserRouter([
        {
            path: "/login",
            element: <LoginPage />,
        },
        {
            path: "/groceries",
            element: <GroceriesPage />,
        },
    ]);


export default router;