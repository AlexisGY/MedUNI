export const ICONS_BY_ID = {
  1: 'bi bi-scissors',
  2: 'bi bi-heart-pulse-fill',
  3: 'bi bi-gender-female',
  4: 'bi bi-gender-male',
  5: 'bi bi-eye-fill',
  6: 'bi bi-capsule',
  7: 'bi bi-chat-square-heart-fill',
  8: 'bi bi-ear-fill',
  9: 'bi bi-emoji-laughing-fill',
  10: 'bi bi-person-hearts',
  11: 'bi bi-flask-fill',
  12: 'bi bi-lungs-fill',
  13: 'bi bi-hospital-fill',
  14: 'bi bi-fork-knife',
  15: 'bi bi-soundwave'
};

export const NOMBRES_BY_ID = {
  1: 'Cirugía General',
  2: 'Cardiología',
  3: 'Ginecología',
  4: 'Urología',
  5: 'Oftalmología',
  6: 'Endocrinología',
  7: 'Psicología',
  8: 'Otorrinolaringología',
  9: 'Odontología',
  10: 'Psiquiatría',
  11: 'Laboratorio Clínico',
  12: 'Neumología',
  13: 'Medicina General',
  14: 'Nutrición',
  15: 'Ecografía',
};

export function getEspecialidadIconClassById(id) {
  return ICONS_BY_ID[id] || 'bi bi-hospital-fill';
}

export function getEspecialidadNombreById(id) {
  return NOMBRES_BY_ID[id] || 'Especialidad';
}

export function getEspecialidadImageById(id) {
  const images = import.meta.glob('/src/assets/especialidades/*.{png,jpg,jpeg,svg}', {
    eager: true,
    import: 'default',
  });

  const candidates = [
    `/src/assets/especialidades/${id}.png`,
    `/src/assets/especialidades/${id}.jpg`,
    `/src/assets/especialidades/${id}.jpeg`,
    `/src/assets/especialidades/${id}.svg`,
  ];

  for (const key of candidates) {
    if (images[key]) return images[key];
  }

  const fallbackSvg = '/src/assets/especialidades/fallback.svg';
  if (images[fallbackSvg]) return images[fallbackSvg];
  return '';
}
export function getEspecialidadMetaById(id) {
  const n = Number(id);
  return {
    id: n,
    nombre: getEspecialidadNombreById(n),
    icono: getEspecialidadIconClassById(n),
    imagen: getEspecialidadImageById(n),
  };
}