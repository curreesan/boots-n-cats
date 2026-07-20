export type Order = {
  id: string;
  user_id: string;
  total_amount: number;
  created_at: string;
};

export type OrderItem = {
  id: string;
  order_id: string;
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: number;
};

export type OrderDetail = {
  order: Order;
  items: OrderItem[];
};
