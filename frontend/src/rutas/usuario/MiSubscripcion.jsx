import React, {useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Box, Typography,Button } from '@mui/material';
import {Dialog, DialogTitle, DialogContent, DialogActions,} from '@mui/material';

import SidenavUsuari from "../../Componentes/Sidenav/UsuariSidenav";
import Navbar from '../../Componentes/NavBar';
import { data, Navigate } from 'react-router-dom';
const BASE_URL = 'http://localhost:8000';

const MiSubscripcio = () => {
  const [rows, setRows] = useState([]);
  const [noSubscription, setNoSubscription] = useState(false);
  const [subscripciones, setSubscripciones] = useState([]);
  const [openSubDialog, setOpenSubDialog] = useState(false);
  const [userSubscription, setUserSubscription] = useState(null);

  const columns = [
    {
      field: 'nom',
      headerName: 'Nombre',
      width: 200,
      editable: false
    },
    {
      field: 'descripcio',
      headerName: 'Descripcion',
      width: 200,
      editable: false
    },
    {
      field: 'preu',
      headerName: 'Precio',
      width: 150,
      editable: false
    },
    {
      field: 'datallancament',
      headerName: 'Fecha de lanzamiento',
      width: 250,
      editable: false
    },
    {
      field: 'qualificacioedat',
      headerName: 'Qualificacion por edat',
      width: 150,
      editable: false
    },
    {
      field: 'desenvolupador',
      headerName: 'Desarrollador',
      width: 370,
      editable: false
    }
  ];
const handleSubscribe = async (tipoNombre) => {
  try {
    const token = localStorage.getItem("token");
    const sobrenom = localStorage.getItem("sobrenom");

    const response = await fetch(`${BASE_URL}/subscripcions/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({
        usuarisobrenom: sobrenom,
        tipussubscripcionom: tipoNombre,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error al suscribirse");
    }

    const data = await response.json();
    alert(`Suscripción al plan ${data.tipussubscripcionom} creada con éxito`);

    setOpenSubDialog(false);
    // Opcional: actualizar la suscripción activa del usuario recargando datos:
    await getSubscripcionsUsuari();

  } catch (error) {
    alert(`Error: ${error.message}`);
  }
};
  const getSubscripcionsUsuari = async () => {
    try {
      const token = localStorage.getItem("token");
      const sobrenom = localStorage.getItem("sobrenom");
      if (!token) throw new Error("No hay token de acceso, inicia sesión.");

      const response = await fetch(`${BASE_URL}/subscripcions/usuari/${sobrenom}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error("Error al obtener las suscripciones");

      const data = await response.json();

      if (!data || Object.keys(data).length == 0) {
        setNoSubscription(true);
        setUserSubscription(null);
      } else {
        setUserSubscription(data[0]);
        setNoSubscription(false);
        return data[0];
      }
    } catch (error) {
      console.error(error);
      setNoSubscription(true);
    }
  };

    const getVideojocs = async (subscripcio) => {
    try {
      const accessToken = localStorage.getItem("token");
      const tipussubscripcionom = subscripcio.tipussubscripcionom;

      const response = await fetch(`${BASE_URL}/tipus_subscripcions/${tipussubscripcionom}/elementsvenda`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      });

      if (!response.ok) throw new Error("Error al obtener los videojuegos");

      const data = await response.json();

      if (data.length == 0) {
        setNoSubscription(true);
        return;
      }

      const rowsConId = data.map((item, index) => ({ id: index, ...item }));
      setRows(rowsConId);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchSubscripciones = async () => {
    try {
      const accessToken = localStorage.getItem("token");

      const response = await fetch(`${BASE_URL}/tipus_subscripcions/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });

      if (!response.ok) throw new Error("Error al obtener tipos de suscripción");

      const data = await response.json();

      const adaptado = data.map((s) => ({
        nombre: s.nom,
        descripcion: s.descripcio,
        precio: `${s.preumensual} €`,
        id: s.nom
      }));

      setSubscripciones(adaptado);
    } catch (error) {
      console.error(error);
    }


  };

  useEffect(() => {
  const fetchData = async () => {
    const subscripcio = await getSubscripcionsUsuari(); // debe devolver la subscripción
    if (subscripcio) {
      await getVideojocs(subscripcio); // le pasas directamente la subscripción
    }
    fetchSubscripciones(); // si no depende de nada, la puedes dejar así
  };

  fetchData();
}, []);

  return (
    <>
    <Navbar/>
    <Box height={40}/>
    <Box sx={{  display: 'flex'}}>
      <SidenavUsuari/>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <h1>Mi subscripcion</h1>
          <div className="subscripcio-container">
            {userSubscription ? (
              <>
                <p><strong>Tipo:</strong> {userSubscription.tipussubscripcionom}</p>
                <p><strong>Fecha de inicio:</strong> {userSubscription.datainici}</p>
                <p><strong>Fecha de fin:</strong> {userSubscription.datafi}</p>
              </>
            ) : null}
          </div>
        <Box height={75}/>
          <Box sx={{ maxWidth: '80vw', margin: '0 auto', alignItems: 'center', width: '100%'}}>
            <div style={{ height: '100%', width: '100%', minHeight:'100px' }}>
              {noSubscription ? (
                <Box textAlign="center" mt={4}>
                  <Typography variant="h6" color="textSecondary">
                    No tienes una suscripción activa.
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    sx={{ mt: 2 }}
                    onClick={() => setOpenSubDialog(true)}
                  >
                    Suscribirse ahora
                  </Button>

                  {/* Diálogo de suscripción */}
                  <Dialog open={openSubDialog} onClose={() => setOpenSubDialog(false)} maxWidth="sm" fullWidth>
                    <DialogTitle>Elige una suscripción</DialogTitle>
                    <DialogContent dividers>
                      {subscripciones.map((sub) => (
                        <Box key={sub.id} mb={3} p={2} border="1px solid #ccc" borderRadius={2}>
                          <Typography variant="h6">{sub.nombre}</Typography>
                          <Typography color="textSecondary">{sub.precio}</Typography>
                          <Typography variant="body2" mt={1}>{sub.descripcion}</Typography>
                          <Button
                            variant="outlined"
                            sx={{ mt: 1 }}
                            onClick={() => handleSubscribe(sub.nombre)}
                          >
                            Elegir
                          </Button>
                        </Box>
                      ))}
                    </DialogContent>
                    <DialogActions>
                      <Button onClick={() => setOpenSubDialog(false)}>Cerrar</Button>
                    </DialogActions>
                  </Dialog>
                </Box>
              ) : (
                <DataGrid
                  rows={rows}
                  columns={columns}
                  getRowId={(row) => row.id}
                  pageSize={10}
                  disableRowSelectionOnClick
                  isCellEditable={() => false}
                />
              )}

            </div>
          </Box>
        </Box>
      </Box>
    </>
  )
}

export default MiSubscripcio;
