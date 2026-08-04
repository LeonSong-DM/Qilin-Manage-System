const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const TOKEN_KEY = 'qilin_pc_token'
const USER_KEY = 'qilin_pc_user'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(data.detail ?? data.message ?? '请求失败')
  }

  return response.json()
}

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
    headers: {
      Authorization: `Bearer ${token}`,
    },
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
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  } catch (error) {
    clearAuth()
    throw error
  }
}
