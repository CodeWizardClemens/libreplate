import axios from "axios";

import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import type {
    Recipe,
    RecipeCreate,
} from "./types";

function getCsrfToken() {
    const cookie = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="));

    return cookie?.split("=")[1];
}

const api = axios.create({
    baseURL: "/api/recipes/",
    withCredentials: true,
});

api.interceptors.request.use((config) => {
    const csrfToken = getCsrfToken();

    if (csrfToken) {
        config.headers["X-CSRFToken"] = csrfToken;
    }

    return config;
});

export const recipeKeys = {
    all: ["recipes"] as const,

    detail: (id: number) =>
        ["recipes", id] as const,
};

export function useRecipes() {
    return useQuery({
        queryKey: recipeKeys.all,

        queryFn: async () => {
            const { data } = await api.get<Recipe[]>("");

            return data;
        },
    });
}

export function useCreateRecipe() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (recipe: RecipeCreate) => {
            const { data } = await api.post<Recipe>(
                "",
                recipe
            );

            return data;
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}

export function useDeleteRecipe() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (id: number) => {
            await api.delete(`${id}/`);
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}

export function useToggleFavorite() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (id: number) => {
            const { data } = await api.post<Recipe>(
                `${id}/toggle-favorite/`
            );

            return data;
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}

export function useTogglePin() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (id: number) => {
            const { data } = await api.post<Recipe>(
                `${id}/toggle-pin/`
            );

            return data;
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}

export function useCopyRecipe() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({
            id,
            name,
        }: {
            id: number;
            name: string;
        }) => {
            const { data } = await api.post<Recipe>(
                `${id}/copy/`,
                {
                    name,
                }
            );

            return data;
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}