import { defineStore } from 'pinia'

export const useCitaStore = defineStore('cita', {
  state: () => ({
    fecha: null,
    hora: null,
    estudianteId: null,
    medicoId: null,
    medicoNombre: null,
    especialidadId: null,
    especialidadNombre: null,
    estado: 'pendiente'
  }),
  actions: {
    setEstudiante(id) {
      this.estudianteId = id;
    },
    setEspecialidad(id) {
      this.especialidadId = id;
    },
    setEspecialidadNombre(nombre) {
      this.nombre = nombre;
    },
    setFecha(fecha) {
      this.fecha = fecha;
    },
    setMedico(id) {
      this.medicoId = id;
    },
    setHora(hora) {
      this.hora = hora;
    },
    reset() {
      this.$reset(); // Resetea todos los valores
    }
  }
})