const API_URL = import.meta.env.VITE_API_URL
const USE_MOCK = !API_URL  // si no hay backend, usa mocks

async function http(path, opts = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
    ...opts,
  })
  if (!res.ok) throw new Error(await res.text() || 'Error de servidor')
  return res.json()
}


/* ---------- AUTH ---------- */
export async function login({ username, password }) {
  // Asegúrate de que el nombre de la variable en el cuerpo de la petición
  // coincida con lo que tu backend espera
  return http('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}
/* ---------- CATÁLOGOS ---------- */
export async function listarEspecialidades() {
  if (USE_MOCK) return ['Odontología','Medicina General','Psicología']
  return http('/especialidades')
}

export async function listarHorarios({ especialidad, fecha }) {
  if (USE_MOCK) {
    const base = ['08:00','08:30','09:00','09:30','10:00','10:30']
    return base.map((h,i)=>({ hora:h, ocupado: (especialidad==='Odontología' && i%2===0) }))
  }
  const q = new URLSearchParams({ especialidad, fecha })
  return http(`/horarios?${q}`)
}
