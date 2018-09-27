window.MathJax = {
  messageStyle: 'none',
  tex2jax: { preview: 'none' },
  showMathMenu: false,
  'fast-preview': { disabled: true }
}

const obtenerApi = () => ({
  generarVisualizacion: pywebview.api.generar_visualizacion,
  mostrarResultados: pywebview.api.mostrar_resultados,
  validarParticiones: pywebview.api.validar_particiones
})

window.app = new Vue({
  el: '#app',
  data: {
    funcion: 'x',
    intervalo: '[0, 1.5]',
    metodo: 'trapecio',
    particiones: '5',
    resultado: {
      esValido: true,
      latex: '\\int_{0}^{1.5}{x}dx'
    },
    resultadoParticiones: {
      esValido: true
    },
    estaEvaluando: false,
    estaValidando: false,
    estaMostrandoResultados: false
  },
  computed: {
    visualizacion() {
      if (this.resultado.esValido)
        return '$$' + this.resultado.latex.replace(/\r/g, 'r') + '$$'
      else
        return ''
    },
    esMetodoTrapecio() {
      return this.metodo === 'trapecio'
    },
    esMetodoSimpson() {
      return !this.esMetodoTrapecio
    },
    errorFuncion() {
      return this.obtenerErroresResultado('funcion')
    },
    errorIntervalo() {
      return this.obtenerErroresResultado('intervalo')
    },
    errorParticiones() {
      return this.obtenerErrores(this.resultadoParticiones.errores, 'particiones')
    },
    puedeEvaluar() {
      return this.resultado.esValido && this.resultadoParticiones.esValido
        && !this.estaEvaluando && !this.estaValidando && !this.estaMostrandoResultados
    }
  },
  watch: {
    funcion() {
      this.computarVisualizacion()
    },
    intervalo() {
      this.computarVisualizacion()
    },
    particiones() {
      this.validarParticiones()
    },
    metodo() {
      this.validarParticiones()
    },
    visualizacion() {
      this.$nextTick(() => MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'formula']))
    }
  },
  methods: {
    obtenerErroresResultado(prop) {
      return this.obtenerErrores(this.resultado.errores, prop)
    },
    obtenerErrores(errores, prop) {
      if (errores !== undefined) {
        var errorPropiedad = undefined

        for (var i = 0; i < errores.length; i++) {
          if (errores[i].propiedad === prop) {
            errorPropiedad = errores[i]
          }
        }

        if (errorPropiedad !== undefined) {
          return {
            tieneError: true,
            mensaje: errorPropiedad.mensaje
          }
        }
      }

      return { tieneError: false }
    },
    computarVisualizacion() {
      app.estaEvaluando = true

      obtenerApi().generarVisualizacion(this._data)
        .then(resultado => {
          app.resultado = resultado
          app.estaEvaluando = false
        }).catch(error => {
          console.error(error)
          alert('Ocurrió un error al comunicarse con el servidor. Reinicie el programa.')
          app.estaEvaluando = false
        })
    },
    validarParticiones() {
      app.estaValidando = true

      obtenerApi().validarParticiones(this._data)
        .then(resultado => {
          app.resultadoParticiones = resultado
          app.estaValidando = false
        }).catch(error => {
          console.error(error)
          alert('Ocurrió un error al comunicarse con el servidor. Reinicie el programa.')
          app.estaEvaluando = false
        })
    },
    mostrarResultados() {
      app.estaMostrandoResultados = true

      obtenerApi().mostrarResultados(this._data)
        .then(() => {
          app.estaMostrandoResultados = false
        }).catch(error => {
          console.error(error)
          alert('Ocurrió un error al comunicarse con el servidor. Reinicie el programa.')
          app.estaMostrandoResultados = false
        })
    }
  }
})