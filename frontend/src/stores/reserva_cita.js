import { defineStore } from 'pinia'

export const useCitaStore = defineStore('cita', {
  state: () => ({
    fecha: null,
    hora: null,
    estudiante_id: null,
    medico_id: null,
    medico_nombre: null,
    especialidad_id: null,
    especialidad_nombre: null,
    estado: 'pendiente'
  }),
  actions: {
    setEstudiante(id) {
      this.estudiante_id = id;
    },
    setEspecialidad(id) {
      this.especialidad_id = id;
    },
    setEspecialidadNombre(nombre) {
      this.especialidad_nombre = nombre;
    },
    setFecha(fecha) {
      this.fecha = fecha;
    },
    setMedico(id) {
      this.medico_id = id;
    },
    setHora(hora) {
      this.hora = hora;
    },
    reset() {
      this.$reset(); // Resetea todos los valores
    }
  }
})