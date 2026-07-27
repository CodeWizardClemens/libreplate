import { client } from "./generated/client.gen";

function getCookie(name: string): string | undefined {
  const value = document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`));

  return value?.split("=")[1];
}

// Required so the browser actually sends the sessionid/csrftoken cookies
// cross-origin (frontend on :5173, backend on :8000). Without this, no
// cookie is ever sent - not a CSRF issue, not an auth-logic issue, just
// missing transport config. This is not app-level "authentication", it's
// the baseline requirement for cookies to move between the two origins.
client.setConfig({
  credentials: "include",
});

// Django's CsrfViewMiddleware rejects unsafe methods (POST/PATCH/PUT/
// DELETE) without a valid X-CSRFToken header, regardless of whether the
// request is otherwise authenticated. This reads the csrftoken cookie
// fresh on every request rather than baking in a single snapshot, so a
// rotated token (e.g. after login) doesn't get sent stale.
client.interceptors.request.use((request) => {
  const csrfToken = getCookie("csrftoken");

  if (csrfToken) {
    request.headers.set("X-CSRFToken", csrfToken);
  }

  return request;
});