import { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, ShoppingCart } from "lucide-react";
import { useAuth } from "../context/useAuth";
import { useCart } from "../context/useCart";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetClose,
} from "@/components/ui/sheet";

function CartLink({ cartCount }: { cartCount: number }) {
  return (
    <Link to="/cart" className="relative flex items-center" aria-label="Cart">
      <ShoppingCart className="size-5" />
      {cartCount > 0 && (
        <span className="absolute -top-2 -right-2 flex size-4 items-center justify-center rounded-full bg-primary text-[10px] font-semibold text-primary-foreground">
          {cartCount}
        </span>
      )}
    </Link>
  );
}

function Navbar() {
  const { user, logout } = useAuth();
  const { items } = useCart();
  const [menuOpen, setMenuOpen] = useState(false);
  const cartCount = items.reduce((sum, line) => sum + line.quantity, 0);

  const navLinkClass = "text-sm font-medium hover:text-primary";

  return (
    <nav className="sticky top-0 z-10 border-b border-border bg-background">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/" className="text-xl font-bold text-primary">
          Boots n&apos; Cats
        </Link>

        {/* Desktop nav */}
        <div className="hidden items-center gap-6 md:flex">
          {user && user.role === "staff" && (
            <div className="flex items-center gap-4 border-r border-border pr-6 text-sm text-muted-foreground">
              <Link to="/admin/catalog" className="hover:text-foreground">
                Catalog
              </Link>
              <Link to="/admin/consultations" className="hover:text-foreground">
                Requests
              </Link>
              <Link to="/admin/knowledge" className="hover:text-foreground">
                Knowledge
              </Link>
            </div>
          )}

          <Link to="/" className={navLinkClass}>
            Home
          </Link>
          <Link to="/products" className={navLinkClass}>
            Products
          </Link>
          <Link to="/pets" className={navLinkClass}>
            Pets
          </Link>

          <CartLink cartCount={cartCount} />

          {user ? (
            <div className="flex items-center gap-4">
              <Link to="/orders" className={navLinkClass}>
                Orders
              </Link>
              <Link to="/account" className={navLinkClass}>
                {user.name}
              </Link>
              <Button variant="outline" size="sm" onClick={() => logout()}>
                Logout
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link to="/login" className={navLinkClass}>
                Login
              </Link>
              <Button asChild size="sm">
                <Link to="/register">Register</Link>
              </Button>
            </div>
          )}
        </div>

        {/* Mobile nav */}
        <div className="flex items-center gap-4 md:hidden">
          <CartLink cartCount={cartCount} />
          <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
            <Button
              variant="ghost"
              size="icon"
              aria-label="Open menu"
              onClick={() => setMenuOpen(true)}
            >
              <Menu className="size-5" />
            </Button>
            <SheetContent side="right" className="w-72">
              <SheetHeader>
                <SheetTitle>Menu</SheetTitle>
              </SheetHeader>
              <div className="flex flex-col gap-4 px-4">
                <SheetClose asChild>
                  <Link to="/" className={navLinkClass}>
                    Home
                  </Link>
                </SheetClose>
                <SheetClose asChild>
                  <Link to="/products" className={navLinkClass}>
                    Products
                  </Link>
                </SheetClose>
                <SheetClose asChild>
                  <Link to="/pets" className={navLinkClass}>
                    Pets
                  </Link>
                </SheetClose>

                {user && user.role === "staff" && (
                  <div className="flex flex-col gap-4 border-t border-border pt-4 text-sm text-muted-foreground">
                    <SheetClose asChild>
                      <Link to="/admin/catalog" className="hover:text-foreground">
                        Admin: Catalog
                      </Link>
                    </SheetClose>
                    <SheetClose asChild>
                      <Link to="/admin/consultations" className="hover:text-foreground">
                        Admin: Requests
                      </Link>
                    </SheetClose>
                    <SheetClose asChild>
                      <Link to="/admin/knowledge" className="hover:text-foreground">
                        Admin: Knowledge
                      </Link>
                    </SheetClose>
                  </div>
                )}

                <div className="flex flex-col gap-4 border-t border-border pt-4">
                  {user ? (
                    <>
                      <SheetClose asChild>
                        <Link to="/orders" className={navLinkClass}>
                          Orders
                        </Link>
                      </SheetClose>
                      <SheetClose asChild>
                        <Link to="/account" className={navLinkClass}>
                          {user.name}
                        </Link>
                      </SheetClose>
                      <Button variant="outline" onClick={() => logout()}>
                        Logout
                      </Button>
                    </>
                  ) : (
                    <>
                      <SheetClose asChild>
                        <Link to="/login" className={navLinkClass}>
                          Login
                        </Link>
                      </SheetClose>
                      <SheetClose asChild>
                        <Button asChild>
                          <Link to="/register">Register</Link>
                        </Button>
                      </SheetClose>
                    </>
                  )}
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
