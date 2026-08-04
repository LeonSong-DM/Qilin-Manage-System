const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export const TOKEN_KEY = 'qilin_pc_token'
export const USER_KEY = 'qilin_pc_user'
export const AUTH_EXPIRED_EVENT = 'qilin:auth-expired'

function expireAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  window.dispatchEvent(new Event(AUTH_EXPIRED_EVENT))
}

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    if (response.status === 401 && path !== '/users/login') {
      expireAuth()
    }

    throw new Error(data.detail ?? data.message ?? '请求失败')
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export function authHeaders(token) {
  return token
    ? {
        Authorization: `Bearer ${token}`,
      }
    : {}
}
