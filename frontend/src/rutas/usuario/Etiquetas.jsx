import React, { useEffect, useState } from "react";
import Navbar from '../../Componentes/NavBar';
import Sidenav from "../../Componentes/Sidenav/UsuariSidenav";
const BASE_URL = "http://localhost:8000"; // Cambia esto si es necesario

const EtiquetesPerVideojoc = () => {
  const [videojocs, setVideojocs] = useState([]);
  const [etiquetes, setEtiquetes] = useState({});
  const [nuevaEtiqueta, setNuevaEtiqueta] = useState({});
  const [error, setError] = useState("");
  const sobrenom = localStorage.getItem("sobrenom");
  const token = localStorage.getItem("token");

  useEffect(() => {
    // Cargar videojocs comprados por el usuario
    const fetchComprats = async () => {
      const accessToken = localStorage.getItem("token");
      const usuarisobrenom = localStorage.getItem("sobrenom");
      try {
        const response = await fetch(`${BASE_URL}/products/user/${usuarisobrenom}/accessos`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) throw new Error("Error al cargar videojocs comprats");
        const data = await response.json();
        const rowsConId = data.products.map((item, index) => ({ id: index, ...item }));
        setVideojocs(rowsConId);
      } catch (err) {
        console.error(err);
      }
    };

    fetchComprats();
  }, []);

  useEffect(() => {
    // Cargar etiquetas de cada videojoc
    videojocs.forEach((vj) => {
      fetch(`${BASE_URL}/etiquetes/${vj.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => {
          if (!res.ok) throw new Error("No hi ha etiquetes");
          return res.json();
        })
        .then((data) => {
          setEtiquetes((prev) => ({ ...prev, [vj.id]: data }));
        })
        .catch(() => {
          setEtiquetes((prev) => ({ ...prev, [vj.id]: [] }));
        });
    });
  }, [videojocs]);

  const handleEtiquetaChange = (vjId, value) => {
    setNuevaEtiqueta((prev) => ({ ...prev, [vjId]: value }));
  };

  const afegirEtiqueta = async (vjId) => {
    const etiqueta = nuevaEtiqueta[vjId];
    if (!etiqueta || etiqueta.trim() === "") return;

    try {
      const res = await fetch(`${BASE_URL}/etiquetes/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          videojocid: vjId,
          etiquetanom: etiqueta.trim(),
          usuarisobrenom: sobrenom,
        }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Error en afegir etiqueta");
      }

      // Actualizar etiquetas visualmente
      setEtiquetes((prev) => ({
        ...prev,
        [vjId]: [...(prev[vjId] || []), etiqueta.trim()],
      }));
      setNuevaEtiqueta((prev) => ({ ...prev, [vjId]: "" }));
      setError("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
        <Sidenav/>
        <Navbar/>
      <h2 style={{ textAlign: "center" }}>Etiquetes dels teus videojocs</h2>
      {videojocs.map((vj) => (
        <div
          key={vj.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "1rem",
            marginTop:"3rem",
            marginBottom: "1.5rem",
            backgroundColor: "#f9f9f9",
          }}
        >
          <h3>{vj.nom}</h3>
          <p><strong>Etiquetes:</strong> {etiquetes[vj.id]?.length > 0 ? etiquetes[vj.id].join(", ") : "Encara no hi ha"}</p>

          {etiquetes[vj.id]?.filter((e) => e.usuarisobrenom === sobrenom).length < 5 && (
            <div style={{ display: "flex", gap: "1rem", marginTop: "0.5rem" }}>
              <input
                type="text"
                value={nuevaEtiqueta[vj.id] || ""}
                onChange={(e) => handleEtiquetaChange(vj.id, e.target.value)}
                placeholder="Afegeix una etiqueta"
                style={{ flex: 1, padding: "0.5rem" }}
              />
              <button
                onClick={() => afegirEtiqueta(vj.id)}
                style={{
                  padding: "0.5rem 1rem",
                  backgroundColor: "#007bff",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Afegir
              </button>
            </div>
          )}
        </div>
      ))}
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
    </div>
  );
};

export default EtiquetesPerVideojoc;
