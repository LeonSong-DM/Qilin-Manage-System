const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export const TOKEN_KEY = 'qilin_pc_token'
export const USER_KEY = 'qilin_pc_user'
export const AUTH_EXPIRED_EVENT = 'qilin:auth-expired'

function expireAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  window.dispatchEvent(new Event(AUTH_EXPIRED_EVENT))
}

function formatErrorMessage(data) {
  if (Array.isArray(data.detail)) {
    return data.detail
      .map((item) => {
        const field = Array.isArray(item.loc) ? item.loc.slice(1).join('.') : ''
        return field ? `${field}: ${item.msg}` : item.msg
      })
      .filter(Boolean)
      .join('；')
  }

  return data.detail ?? data.message ?? '请求失败'
}

export async function request(path, options = {}) {
  const { headers, ...restOptions } = options

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...restOptions,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  })

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    if (response.status === 401 && path !== '/users/login') {
      expireAuth()
    }

    throw new Error(formatErrorMessage(data))
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
