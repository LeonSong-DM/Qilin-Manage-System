import { TOKEN_KEY, USER_KEY, authHeaders, request } from './http'

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getStoredUser() {
  const rawUser = localStorage.getItem(USER_KEY)
  if (!rawUser) {
    return null
  }

  try {
    return JSON.parse(rawUser)
  } catch {
    clearAuth()
    return null
  }
}

export function storeAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export async function login(payload) {
  const loginResult = await request('/users/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })

  const token = loginResult.access_token
  const user = await request('/users/me', {
    headers: authHeaders(token),
  })

  return { token, user }
}

export async function getCurrentUser(token = getStoredToken()) {
  if (!token) {
    clearAuth()
    return null
  }

  try {
    return await request('/users/me', {
      headers: authHeaders(token),
    })
  } catch (error) {
    clearAuth()
    throw error
  }
}
