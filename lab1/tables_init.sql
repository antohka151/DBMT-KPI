CREATE TABLE "products" (
  "product_id" int,
  "product_name" varchar(30),
  PRIMARY KEY ("product_id")
);

CREATE TABLE "customers" (
  "customer_id" int,
  "name" varchar(30),
  PRIMARY KEY ("customer_id")
);

CREATE TABLE "orders" (
  "order_id" int,
  "customer_id" int,
  "date" timestamptz,
  "product_id" int,
  PRIMARY KEY ("order_id"),
  CONSTRAINT "FK_orders.customer_id"
    FOREIGN KEY ("customer_id")
      REFERENCES "customers"("customer_id"),
  CONSTRAINT "FK_orders.product_id"
    FOREIGN KEY ("product_id")
      REFERENCES "products"("product_id")
);
