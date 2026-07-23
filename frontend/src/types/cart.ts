export type CartLine = {
  id: string;
  product_id: string;
  product_name: string;
  unit_price: number;
  stock_quantity: number;
  image_url: string | null;
  quantity: number;
};
