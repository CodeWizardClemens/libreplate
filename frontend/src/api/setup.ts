import { client } from "./generated/client.gen";
import { getCsrfToken } from "./csrf";

client.setConfig({
  baseUrl: "http://localhost:8000",
  credentials: "include",
  headers: {
    "X-CSRFToken": getCsrfToken() ?? "",
  },
});