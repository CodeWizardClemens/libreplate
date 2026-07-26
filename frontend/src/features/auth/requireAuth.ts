import {
    redirect,
    type LoaderFunctionArgs,
} from "react-router-dom";

import { getCurrentUser } from "./api/authApi";
import type { User } from "./types";

export async function requireAuth({
    request,
}: LoaderFunctionArgs): Promise<User> {
    const user = await getCurrentUser();

    if (!user) {
        const url = new URL(request.url);

        throw redirect(
            `/login?redirectTo=${encodeURIComponent(
                url.pathname + url.search
            )}`
        );
    }

    return user;
}