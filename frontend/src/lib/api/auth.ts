import { corePost } from "./coreClient";

export type UserCreate = {
  firstName: string;
  lastName?: string;
  email: string;
  mobile: string;
  whatsappMobile?: string;
  password: string;
};

export type OtpPendingResponse = {
  userId: string;
  otpId: string;
  message: string;
};

export type TokenResponse = {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
};

export const register = (data: UserCreate) => corePost<OtpPendingResponse>("/auth/register", data, false);

export const verifyRegister = (otpId: string, code: string) =>
  corePost<TokenResponse>("/auth/register/verify", { otpId, code }, false);

export const login = (email: string, password: string) =>
  corePost<OtpPendingResponse>("/auth/login", { email, password }, false);

export const verifyLogin = (otpId: string, code: string) =>
  corePost<TokenResponse>("/auth/login/verify", { otpId, code }, false);
