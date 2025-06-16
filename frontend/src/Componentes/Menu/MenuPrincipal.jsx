import './MenuPrincipal.css'
import Inicio from '../../rutas/usuario/Biblioteca'
import Perfil from '../../rutas/usuario/perfil'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import LoginRegistro from '../Login/LoginRegistro'

const MenuPrincipal = () =>{
return(
    <Router>
        <Routes>
            <Route>
                <Route path='/Inicio' element = {<Inicio/>}/>
                <Route path='/Perfil' element= {<Perfil/>}/>
            </Route>    
        <Route path='/' element = {<LoginRegistro/>}/>    
        </Routes>
        
    </Router>
);

};

export default MenuPrincipal;