export function fetchWithAuth(input: RequestInfo, init: RequestInit = {}) {
  const token = localStorage.getItem('gc_access_token');
  const headers = new Headers(init.headers || {});
  headers.set('Content-Type', headers.get('Content-Type') || 'application/json');
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  return fetch(input, { ...init, headers });
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem('gc_access_token', token);
  else localStorage.removeItem('gc_access_token');
}

export function getToken() {
  return localStorage.getItem('gc_access_token');
}
