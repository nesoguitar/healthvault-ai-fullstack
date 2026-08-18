import { apiFetch } from "./client";

export interface RegisterPayload {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserOut {
  id: string;
  email: string;
  is_active: boolean;
  is_verified: boolean;
  mfa_enabled: boolean;
}

export const authApi = {
  register: (payload: RegisterPayload) =>
    apiFetch<UserOut>("/auth/register", { method: "POST", body: payload, skipAuth: true }),

  login: (email: string, password: string) =>
    apiFetch<TokenPair>("/auth/login", { method: "POST", body: { email, password }, skipAuth: true }),

  me: () => apiFetch<UserOut>("/auth/me"),
};
