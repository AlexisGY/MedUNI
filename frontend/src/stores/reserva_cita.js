import { defineStore } from 'pinia'

export const useCitaStore = defineStore('cita', {
  state: () => ({
    fecha: null,
    hora: null,
    estudiante_id: null,
    medico_id: null,
    especialidad_id: null,
    estado: 'pendiente'
  }),
  actions: {
    setEstudiante(id) {
      this.estudiante_id = id;
    },
    setEspecialidad(id) {
      this.especialidad_id = id;
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