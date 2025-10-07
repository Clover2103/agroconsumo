import React, { useState } from "react";
import Swal from "sweetalert2";
import "./PrimaryForm.css";

const PrimaryForm = () => {
  const [formData, setFormData] = useState({
    tipoCultivo: "",
    etapaCultivo: "",
    superficie: "",
    tipoSuelo: "",
    humedad: "",
    precipitacion: "",
    temperatura: "",
    radiacionSolar: "",
    velocidadViento: "",
    profundidadRaiz: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validación básica
    for (let key in formData) {
      if (formData[key] === "") {
        Swal.fire({
          icon: "warning",
          title: "Campo vacío",
          text: `Por favor completa el campo "${key}".`,
        });
        return;
      }
    }

    try {
      setLoading(true);

      const response = await fetch("http://127.0.0.1:8000/api/riego/calcular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error("Error al comunicarse con el servidor");

      const data = await response.json();
      console.log("Respuesta del backend:", data);

      Swal.fire({
        icon: "success",
        title: "✅ Recomendaciones para tu cultivo",
        html: `
          <div style="text-align:left;">
            <p>Según tus datos, el sistema generó las siguientes recomendaciones:</p>

            <div style="background:#eef9ff; padding:12px; border-radius:8px; margin-bottom:10px;">
              <b>💧 Recomendación general:</b><br/>
              ${data.recomendacion}
            </div>

            <div style="margin-bottom:10px;">
              <b>🌿 Frecuencia de riego:</b> ${data.frecuencia_riego}<br/>
              <small style="color:gray;">(Cada cuánto aplicar riego para mantener la humedad óptima.)</small>
            </div>

            <div style="margin-bottom:10px;">
              <b>🚿 Volumen recomendado:</b> ${data.volumen_riego_recomendado} m³/ha<br/>
              <small style="color:gray;">(Cantidad total de agua que deberías aplicar por jornada de riego.)</small>
            </div>

            <hr/>

            <div style="margin-bottom:8px;">
              <b>☀️ Evapotranspiración de referencia (ET₀):</b> ${data.ET0_mm_per_day} mm/día<br/>
              <small style="color:gray;">(Pérdida de agua por evaporación y transpiración en condiciones estándar.)</small>
            </div>

            <div style="margin-bottom:8px;">
              <b>🌱 Evapotranspiración del cultivo (ETc):</b> ${data.ETc_mm_per_day} mm/día<br/>
              <small style="color:gray;">(Cantidad de agua que tu cultivo necesita según su tipo y etapa.)</small>
            </div>

            <div style="margin-bottom:8px;">
              <b>📉 Requerimiento neto de riego:</b> ${data.RequerimientoNeto_mm} mm<br/>
              <small style="color:gray;">(Agua que debes reponer al suelo para evitar estrés hídrico.)</small>
            </div>

            <hr/>
            <p>
              🌾 <b>Consejo práctico:</b> Ajusta la frecuencia y el volumen de riego si hay cambios de clima
              (altas temperaturas, lluvias o vientos). Estos factores afectan las necesidades hídricas del cultivo.
            </p>
          </div>
        `,
        confirmButtonText: "Entendido ✅",
        confirmButtonColor: "#28a745",
        width: 600,
      });
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "No se pudo obtener respuesta del servidor.",
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="primary-form">
      <div className="primary-form__content">
        <h3 className="primary-form__title">CONOZCAMOS MÁS TU CULTIVO</h3>
        <p className="mb-4">
          DILIGENCIA EL SIGUIENTE FORMULARIO PARA CALCULAR LAS NECESIDADES DE AGUA
          EN TU CULTIVO. (<span className="color-red">*</span> Campos obligatorios)
        </p>

        <form onSubmit={handleSubmit} className="text-start">

          {/* DATOS DEL CULTIVO */}
          <h5>DATOS DEL CULTIVO</h5>
          <div className="row mb-4 g-2">
            <div className="col-md-6">
              <div className="form-floating">
                <select
                  className="form-select"
                  id="tipoCultivo"
                  value={formData.tipoCultivo}
                  onChange={handleChange}
                >
                  <option value="">-</option>
                  <option value="1">Maíz</option>
                  <option value="2">Arroz</option>
                  <option value="3">Café</option>
                </select>
                <label htmlFor="tipoCultivo">
                  Tipo de cultivo <span className="color-red">*</span>
                </label>
              </div>
            </div>

            <div className="col-md-6">
              <div className="form-floating">
                <select
                  className="form-select"
                  id="etapaCultivo"
                  value={formData.etapaCultivo}
                  onChange={handleChange}
                >
                  <option value="">-</option>
                  <option value="1">Siembra</option>
                  <option value="2">Crecimiento</option>
                  <option value="3">Cosecha</option>
                </select>
                <label htmlFor="etapaCultivo">
                  Etapa del cultivo <span className="color-red">*</span>
                </label>
              </div>
            </div>

            <div className="col-md-6">
              <div className="form-floating">
                <input
                  type="number"
                  className="form-control"
                  id="superficie"
                  value={formData.superficie}
                  onChange={handleChange}
                />
                <label htmlFor="superficie">
                  Superficie sembrada (ha) <span className="color-red">*</span>
                </label>
              </div>
            </div>

            <div className="col-md-6">
              <div className="form-floating">
                <input
                  type="number"
                  className="form-control"
                  id="profundidadRaiz"
                  value={formData.profundidadRaiz}
                  onChange={handleChange}
                />
                <label htmlFor="profundidadRaiz">
                  Profundidad de raíz (cm) <span className="color-red">*</span>
                </label>
              </div>
            </div>
          </div>

          {/* CONDICIONES DEL SUELO */}
          <h5>CONDICIONES DEL SUELO</h5>
          <div className="row mb-4 g-2">
            <div className="col-md-6">
              <div className="form-floating">
                <select
                  className="form-select"
                  id="tipoSuelo"
                  value={formData.tipoSuelo}
                  onChange={handleChange}
                >
                  <option value="">-</option>
                  <option value="1">Arenoso</option>
                  <option value="2">Arcilloso</option>
                  <option value="3">Franco</option>
                </select>
                <label htmlFor="tipoSuelo">
                  Tipo de suelo <span className="color-red">*</span>
                </label>
              </div>
            </div>

            <div className="col-md-6">
              <div className="form-floating">
                <input
                  type="number"
                  className="form-control"
                  id="humedad"
                  value={formData.humedad}
                  onChange={handleChange}
                />
                <label htmlFor="humedad">
                  Humedad del suelo (%) <span className="color-red">*</span>
                </label>
              </div>
            </div>
          </div>

          {/* CONDICIONES CLIMÁTICAS */}
          <h5>CONDICIONES CLIMÁTICAS</h5>
          <div className="row mb-4 g-2">
            <div className="col-md-6">
              <div className="form-floating">
                <select
                  className="form-select"
                  id="precipitacion"
                  value={formData.precipitacion}
                  onChange={handleChange}
                >
                  <option value="">-</option>
                  <option value="1">Baja</option>
                  <option value="2">Media</option>
                  <option value="3">Alta</option>
                </select>
                <label htmlFor="precipitacion">
                  Precipitación <span className="color-red">*</span>
                </label>
              </div>
            </div>

            <div className="col-md-6">
              <div className="form-floating">
                <input
                  type="number"
                  className="form-control"
                  id="temperatura"
                  value={formData.temperatura}
                  onChange={handleChange}
                />
                <label htmlFor="temperatura">
                  Temperatura promedio (°C) <span className="color-red">*</span>
                </label>
              </div>
            </div>

            <div className="col-md-6">
              <div className="form-floating">
                <input
                  type="number"
                  className="form-control"
                  id="radiacionSolar"
                  value={formData.radiacionSolar}
                  onChange={handleChange}
                />
                <label htmlFor="radiacionSolar">
                  Radiación solar (MJ/m²/día) <span className="color-red">*</span>
                </label>
              </div>
            </div>

            <div className="col-md-6">
              <div className="form-floating">
                <input
                  type="number"
                  className="form-control"
                  id="velocidadViento"
                  value={formData.velocidadViento}
                  onChange={handleChange}
                />
                <label htmlFor="velocidadViento">
                  Velocidad del viento (m/s) <span className="color-red">*</span>
                </label>
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-dark w-100"
            disabled={loading}
          >
            {loading ? "Calculando..." : "CONSULTAR"}
          </button>
        </form>
      </div>
    </div>
  );
};

export { PrimaryForm };
