import React, { useEffect, useState } from 'react';
import { TextField, Button, Box, Typography, Rating } from '@mui/material';
import SidenavUsuari from "../../Componentes/Sidenav/UsuariSidenav";
import Navbar from '../../Componentes/NavBar';

const BASE_URL = 'http://localhost:8000';
const Opiniones = () => {
  const [videojocs, setVideojocs] = useState([]);
  const [opinions, setOpinions] = useState({});

 useEffect(() => {
    const getVideojocs = async (event) => {
      try {
        const accessToken = localStorage.getItem("token");
        const usuarisobrenom = localStorage.getItem("sobrenom");

        const response = await fetch(`${BASE_URL}/vendes/usuari/${usuarisobrenom}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${accessToken}`
          }
        })

      if (!response.ok) {
        throw new Error("Error al obtener los videojuegos");
      }

      const data = await response.json();
      setVideojocs(data);

    } catch (error) {
      console.error(error);
    }
  };

  getVideojocs();
}, []);

  const handleOpinionChange = (id, field, value) => {
    setOpinions(prev => ({
      ...prev,
      [id]: { ...prev[id], [field]: value }
    }));
  };

  const enviarOpinion = async (idJoc) => {
    const token = localStorage.getItem("token");
    const sobrenom = localStorage.getItem("sobrenom");
    const opinion = opinions[idJoc];

    if (!opinion?.text || !opinion?.valoracio) {
      alert("Debes escribir una opinión y una valoración.");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/opinions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          usuarisobrenom: sobrenom,
          videojoc_id: idJoc,
          elementvendaid: opinion.text,
          puntuacio: opinion.valoracio
        })
      });

      if (!response.ok) throw new Error("Error al enviar la opinión");
      alert("Opinión enviada correctamente");
    } catch (error) {
      console.error(error);
      alert("Error al enviar la opinión");
    }
  };

  return (
    
    <Box sx={{ p: 4 }}>
        <Navbar/>
        <SidenavUsuari/>
      <Typography variant="h4" gutterBottom>Opiniones sobre tus videojuegos</Typography>
      {videojocs.map((joc) => (
        <Box key={joc.id} sx={{ mb: 4, border: '1px solid #ccc', p: 2, borderRadius: 2 }}>
          <Typography variant="h6">{joc.Nom}</Typography>
          <TextField
            label="Tu opinión"
            multiline
            fullWidth
            rows={3}
            value={opinions[joc.id]?.text || ''}
            onChange={(e) => handleOpinionChange(joc.id, 'text', e.target.value)}
            sx={{ mt: 2 }}
          />
          <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
            <Rating
              name={`valoracio-${joc.id}`}
              value={opinions[joc.id]?.valoracio || 0}
              onChange={(event, newValue) => handleOpinionChange(joc.id, 'valoracio', newValue)}
            />
            <Button variant="contained" color="primary" sx={{ ml: 2 }} onClick={() => enviarOpinion(joc.id)}>
              Enviar
            </Button>
          </Box>
        </Box>
      ))}
    </Box>
  );
};

export default Opiniones;
