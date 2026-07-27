import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://localhost:8000/api/schema/",
  output: {
    path: "src/api/generated",
  },
});
