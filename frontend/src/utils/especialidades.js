// Mapeos y utilidades para Especialidades

export const ICONS_BY_ID = {
  1: 'bi bi-scissors',                 // Cirugía General
  2: 'bi bi-heart-pulse-fill',         // Cardiología
  3: 'bi bi-gender-female',            // Ginecología
  4: 'bi bi-gender-male',              // Urología
  5: 'bi bi-eye-fill',                 // Oftalmología
  6: 'bi bi-capsule',                  // Endocrinología
  7: 'bi bi-chat-square-heart-fill',   // Psicología 
  8: 'bi bi-ear-fill',                 // Otorrinolaringología
  9: 'bi bi-emoji-laughing-fill',      // Odontología 
  10: 'bi bi-person-hearts',           // Psiquiatría
  11: 'bi bi-flask-fill',              // Laboratorio Clínico
  12: 'bi bi-lungs-fill',              // Neumología 
  13: 'bi bi-hospital-fill',           // Medicina Interna/Familia/General 
  14: 'bi bi-fork-knife',              // Nutrición
  15: 'bi bi-soundwave'                // Ecografía
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
  // Carga todas las imágenes disponibles y retorna la URL (string) directamente
  const images = import.meta.glob('/src/assets/especialidades/*.{png,jpg,jpeg,svg}', {
    eager: true,
    import: 'default',
  });

  // Probar con varias extensiones en orden de preferencia
  const candidates = [
    `/src/assets/especialidades/${id}.png`,
    `/src/assets/especialidades/${id}.jpg`,
    `/src/assets/especialidades/${id}.jpeg`,
    `/src/assets/especialidades/${id}.svg`,
  ];

  for (const key of candidates) {
    if (images[key]) return images[key];
  }

  // Fallback único en SVG (según preferencia actual)
  const fallbackSvg = '/src/assets/especialidades/fallback.svg';
  if (images[fallbackSvg]) return images[fallbackSvg];
  return '';
}