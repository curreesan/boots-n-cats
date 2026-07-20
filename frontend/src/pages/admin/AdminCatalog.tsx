import AdminProducts from "../../components/admin/AdminProducts";
import AdminPets from "../../components/admin/AdminPets";

function AdminCatalog() {
  return (
    <div>
      <h1>Admin: Catalog</h1>
      <AdminProducts />
      <AdminPets />
    </div>
  );
}

export default AdminCatalog;
