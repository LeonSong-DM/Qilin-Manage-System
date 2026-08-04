import { authHeaders, request } from './http'
import { getStoredToken } from './auth'

function authorizedRequest(path) {
  return request(path, {
    headers: authHeaders(getStoredToken()),
  })
}

export async function getClients({ skip = 0, limit = 100 } = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  return authorizedRequest(`/clients/?${params.toString()}`)
}

export async function getUnits({ skip = 0, limit = 100 } = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  return authorizedRequest(`/units/?${params.toString()}`)
}

export async function getProcessMethods({ skip = 0, limit = 100 } = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  return authorizedRequest(`/process-methods/?${params.toString()}`)
}

export async function getProcessOptions(processMethodId, { skip = 0, limit = 100 } = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  return authorizedRequest(
    `/process-methods/${processMethodId}/options?${params.toString()}`,
  )
}

export async function getOrderReferences() {
  const [clients, units, processMethods] = await Promise.all([
    getClients(),
    getUnits(),
    getProcessMethods(),
  ])

  const optionResults = await Promise.allSettled(
    processMethods.map((method) => getProcessOptions(method.id)),
  )
  const processOptions = optionResults.flatMap((result) =>
    result.status === 'fulfilled' ? result.value : [],
  )

  return {
    clients,
    units,
    processMethods,
    processOptions,
  }
}
