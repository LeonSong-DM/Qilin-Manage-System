const TOKEN_KEY = 'qilin_pc_token'
const USER_KEY = 'qilin_pc_user'

export type UserRole = 'admin' | 'employee'
export type UserStatus = 'normal' | 'forbidden'

export interface CurrentUser {
  id: number
  user_number: string
  name: string
  phone_number: string
  role: UserRole
  status: UserStatus
}

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getStoredUser(): CurrentUser | null {
  const rawUser = localStorage.getItem(USER_KEY)
  if (!rawUser) {
    return null
  }

  try {
    return JSON.parse(rawUser) as CurrentUser
  } catch {
    clearAuth()
    return null
  }
}

export function storeAuth(token: string, user: CurrentUser) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}
