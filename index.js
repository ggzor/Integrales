'use strict';

window.MathJax = {
  messageStyle: 'none',
  tex2jax: { preview: 'none' },
  showMathMenu: false,
  'fast-preview': { disabled: true }
};

var obtenerApi = function obtenerApi() {
  return {
    generarVisualizacion: pywebview.api.generar_visualizacion,
    mostrarResultados: pywebview.api.mostrar_resultados,
    validarParticiones: pywebview.api.validar_particiones
  };
};

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
    visualizacion: function visualizacion() {
      if (this.resultado.esValido) return '$$' + this.resultado.latex.replace(/\r/g, 'r') + '$$';else return '';
    },
    esMetodoTrapecio: function esMetodoTrapecio() {
      return this.metodo === 'trapecio';
    },
    esMetodoSimpson: function esMetodoSimpson() {
      return !this.esMetodoTrapecio;
    },
    errorFuncion: function errorFuncion() {
      return this.obtenerErroresResultado('funcion');
    },
    errorIntervalo: function errorIntervalo() {
      return this.obtenerErroresResultado('intervalo');
    },
    errorParticiones: function errorParticiones() {
      return this.obtenerErrores(this.resultadoParticiones.errores, 'particiones');
    },
    puedeEvaluar: function puedeEvaluar() {
      return this.resultado.esValido && this.resultadoParticiones.esValido && !this.estaEvaluando && !this.estaValidando && !this.estaMostrandoResultados;
    }
  },
  watch: {
    funcion: function funcion() {
      this.computarVisualizacion();
    },
    intervalo: function intervalo() {
      this.computarVisualizacion();
    },
    particiones: function particiones() {
      this.validarParticiones();
    },
    metodo: function metodo() {
      this.validarParticiones();
    },
    visualizacion: function visualizacion() {
      this.$nextTick(function () {
        return MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'formula']);
      });
    }
  },
  methods: {
    obtenerErroresResultado: function obtenerErroresResultado(prop) {
      return this.obtenerErrores(this.resultado.errores, prop);
    },
    obtenerErrores: function obtenerErrores(errores, prop) {
      if (errores !== undefined) {
        var errorPropiedad = undefined;

        for (var i = 0; i < errores.length; i++) {
          if (errores[i].propiedad === prop) {
            errorPropiedad = errores[i];
          }
        }

        if (errorPropiedad !== undefined) {
          return {
            tieneError: true,
            mensaje: errorPropiedad.mensaje
          };
        }
      }

      return { tieneError: false };
    },
    computarVisualizacion: function computarVisualizacion() {
      app.estaEvaluando = true;

      obtenerApi().generarVisualizacion(this._data).then(function (resultado) {
        app.resultado = resultado;
        app.estaEvaluando = false;
      }).catch(function (error) {
        console.error(error);
        alert('Ocurrió un error al comunicarse con el servidor. Reinicie el programa.');
        app.estaEvaluando = false;
      });
    },
    validarParticiones: function validarParticiones() {
      app.estaValidando = true;

      obtenerApi().validarParticiones(this._data).then(function (resultado) {
        app.resultadoParticiones = resultado;
        app.estaValidando = false;
      }).catch(function (error) {
        console.error(error);
        alert('Ocurrió un error al comunicarse con el servidor. Reinicie el programa.');
        app.estaEvaluando = false;
      });
    },
    mostrarResultados: function mostrarResultados() {
      app.estaMostrandoResultados = true;

      obtenerApi().mostrarResultados(this._data).then(function () {
        app.estaMostrandoResultados = false;
      }).catch(function (error) {
        console.error(error);
        alert('Ocurrió un error al comunicarse con el servidor. Reinicie el programa.');
        app.estaMostrandoResultados = false;
      });
    }
  }
});