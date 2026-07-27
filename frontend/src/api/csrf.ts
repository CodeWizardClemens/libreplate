export function getCookie(name: string): string | undefined {
  const value = document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`));

  return value?.split("=")[1];
}

export function getCsrfToken(): string | undefined {
  return getCookie("csrftoken");
}
