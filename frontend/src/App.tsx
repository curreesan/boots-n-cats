import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";

import Home from "./pages/Home";

import Products from "./pages/Products";
import ProductDetail from "./pages/ProductDetail";

import Pets from "./pages/Pets";
import PetDetail from "./pages/PetDetail";

import Cart from "./pages/Cart";

import Orders from "./pages/Orders";
import OrderDetail from "./pages/OrderDetail";

import Account from "./pages/Account";
import Login from "./pages/Login";
import Register from "./pages/Register";

import AdminRoute from "./components/AdminRoute";
import AdminCatalog from "./pages/admin/AdminCatalog";
import AdminConsultations from "./pages/admin/AdminConsultations";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="products" element={<Products />} />
          <Route path="products/:id" element={<ProductDetail />} />

          <Route path="pets" element={<Pets />} />
          <Route path="pets/:id" element={<PetDetail />} />

          <Route path="cart" element={<Cart />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />

          <Route element={<ProtectedRoute />}>
            <Route path="orders" element={<Orders />} />
            <Route path="orders/:id" element={<OrderDetail />} />
            <Route path="account" element={<Account />} />
          </Route>

          <Route element={<AdminRoute />}>
            <Route path="admin/catalog" element={<AdminCatalog />} />
            <Route
              path="admin/consultations"
              element={<AdminConsultations />}
            />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
