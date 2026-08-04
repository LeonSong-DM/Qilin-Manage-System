import { http } from './http'
import type { CurrentUser } from './authStorage'

export interface LoginPayload {
  phone_number: string
  password: string
}

export interface LoginResult {
  access_token: string
  token_type: string
}

export async function login(payload: LoginPayload) {
  const loginResponse = await http.post<LoginResult>('/users/login', payload)
  const token = loginResponse.data.access_token
  const userResponse = await http.get<CurrentUser>('/users/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return {
    token,
    user: userResponse.data,
  }
}
