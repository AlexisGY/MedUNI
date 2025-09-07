const API_URL = import.meta.env.VITE_API_URL
const USE_MOCK = !API_URL  // si no hay backend, usa mocks

async function http(path, opts = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
    ...opts,
  })

  const raw = await res.text() // leemos una sola vez
  // Intentamos parsear (si es JSON válido)
  let data = null
  if (raw) {
    try { data = JSON.parse(raw) } catch { /* texto plano */ }
  }

  if (!res.ok) {
    const msg = (data && (data.detail || data.message || data.error)) || raw || 'Error de servidor'
    throw new Error(msg)
  }

  // Éxito: si no había cuerpo devolvemos null
  return data
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
/* ---------- DATOS DEL USUARIO QUE INGRESÓ AL SISTEMA JHARO_BACKEND---------- */
export async function fetchUsuario(username) {
  // Eliminar las comillas dobles al principio y al final del username, si las hay
  username = username.replace(/^"|"$/g, '');

  // Asegúrate de codificar correctamente el username
  const encodedUsername = encodeURIComponent(username);
  return http(`/auth/me?username=${encodedUsername}`);
} 

/* ---------- CATÁLOGOS ---------- */
export async function listarEspecialidades() {
  if (USE_MOCK) return ['Odontología','Medicina General','Psicología']
  return http('/especialidades')
}
// ESPECIALIDADES JHARO BACKEND
export async function fetchEspecialidades() {
  return http('/especialidades'); // devuelve [{ id, nombre, estado }]
}
// DIAS DISPONIBLES JHARO BACKEND
export async function fetchDiasDisponibles(especialidadId) {
  return http(`/disponibilidad/${especialidadId}`);}

  // MEDICOS JHARO BACKEND
export async function fetchMedicosPorEspecialidad(idEspecialidad) {
  return http(`/medicos/especialidad/${idEspecialidad}`);
}
  // HORARIOS JHARO_BACKEND
export async function fetchHorariosPorMedico(fecha, medico_id) {
  return http(`/horarios/${medico_id}/${fecha}`);
}
  // RESERVAR CITA JHARO_BACKEND
export async function reservarCita(citaData) {
  return http('/citas/reservar', {
    method: 'POST',
    body: JSON.stringify(citaData),
  });
}

// OTROS ALEXIS
export async function listarHorarios({ especialidad, fecha }) {
  if (USE_MOCK) {
    const base = ['08:00','08:30','09:00','09:30','10:00','10:30']
    return base.map((h,i)=>({ hora:h, ocupado: (especialidad==='Odontología' && i%2===0) }))
  }
  const q = new URLSearchParams({ especialidad, fecha })
  return http(`/horarios?${q}`)
}
