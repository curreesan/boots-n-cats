import AdminProducts from "../../components/admin/AdminProducts";
import AdminPets from "../../components/admin/AdminPets";

function AdminCatalog() {
  return (
    <div className="flex flex-col gap-8 py-10">
      <h1 className="text-3xl font-bold">Admin: Catalog</h1>
      <AdminProducts />
      <AdminPets />
    </div>
  );
}

export default AdminCatalog;
