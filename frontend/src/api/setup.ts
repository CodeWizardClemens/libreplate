// setup.ts
import { client } from "./generated/client.gen";

client.setConfig({
  baseUrl: "http://localhost:8000",
  credentials: "include",
});