const API_URL = import.meta.env.VITE_API_URL
const USE_MOCK = !API_URL  // si no hay backend, usa mocks

async function http(path, opts = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
    ...opts,
  })

  const raw = await res.text()
  let data = null
  if (raw) { try { data = JSON.parse(raw) } catch {} }

  if (!res.ok) {
    let msg = 'Error de servidor'

    if (data) {
      if (typeof data === 'string') {
        msg = data
      } else if (typeof data.detail === 'string') {
        // FastAPI: detail como string
        msg = data.detail
      } else if (Array.isArray(data.detail)) {
        // FastAPI: detail como array de validaciones
        msg = data.detail
          .map(e => e?.msg || e?.message || (e?.loc ? e.loc.join('.') : JSON.stringify(e)))
          .join(' | ')
      } else if (data.message || data.error) {
        msg = data.message || data.error
      } else {
        // último recurso: stringify
        msg = JSON.stringify(data)
      }
    } else if (raw) {
      msg = raw
    } else {
      msg = `${res.status} ${res.statusText}`
    }

    console.error('HTTP ERROR', res.status, path, msg, data)
    throw new Error(String(msg)) // <-- asegurar string
  }

  return data
}


/* ---------- AUTH ---------- */
export async function login({ username, password }) {
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
  // CITAS DEL USUARIO
export async function fetchCitasPorEstudiante(usuarioId) {
  try {
    return await http(`/citas/citas_reservadas/${usuarioId}`)
  } catch (e) {
    if (e.message?.toLowerCase?.().includes('no hay citas')) return [] 
    return []
  }
}
export async function cancelarCitaPorId(citaId) {
  try {
    const response = await http(`/citas/cancelar_cita/${citaId}`, { method: 'DELETE' })
    return response  // Devuelve la respuesta exitosa
  } catch (e) {
    console.error('Error al cancelar la cita:', e)
    return { message: 'Error al cancelar la cita' }
  }
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
