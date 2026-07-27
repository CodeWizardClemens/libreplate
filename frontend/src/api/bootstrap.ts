import { client } from "./generated/client.gen";

export async function initApi() {
  await client.get({
    url: "/api/accounts/csrf/",
  });

  client.setConfig({
    credentials: "include",
    headers: {
      "X-CSRFToken":
        document.cookie
          .split("; ")
          .find((row) => row.startsWith("csrftoken="))
          ?.split("=")[1] ?? "",
    },
  });
}