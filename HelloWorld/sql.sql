BEGIN;
--
-- Create model Seller
--
CREATE TABLE "Account_seller" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_enterprise" bool NOT NULL);
--
-- Create model Account
--
CREATE TABLE "Account_account" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "username" varchar(40) NOT NULL UNIQUE, "gender" varchar(20) NULL, "mobile" integer NULL, "is_admin" bool NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL, "address_id" integer NULL REFERENCES "Info_address" ("id"));
CREATE TABLE "Account_account_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "account_id" integer NOT NULL REFERENCES "Account_account" ("id"), "group_id" integer NOT NULL REFERENCES "auth_group" ("id"));
CREATE TABLE "Account_account_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "account_id" integer NOT NULL REFERENCES "Account_account" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"));
--
-- Add field account to seller
--
ALTER TABLE "Account_seller" RENAME TO "Account_seller__old";
CREATE TABLE "Account_seller" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_enterprise" bool NOT NULL, "account_id" integer NOT NULL REFERENCES "Account_account" ("id"));
INSERT INTO "Account_seller" ("is_enterprise", "id", "account_id") SELECT "is_enterprise", "id", NULL FROM "Account_seller__old";
DROP TABLE "Account_seller__old";
CREATE INDEX "Account_account_ea8e5d12" ON "Account_account" ("address_id");
CREATE UNIQUE INDEX "Account_account_groups_account_id_4c100dc3_uniq" ON "Account_account_groups" ("account_id", "group_id");
CREATE INDEX "Account_account_groups_8a089c2a" ON "Account_account_groups" ("account_id");
CREATE INDEX "Account_account_groups_0e939a4f" ON "Account_account_groups" ("group_id");
CREATE UNIQUE INDEX "Account_account_user_permissions_account_id_50e554d8_uniq" ON "Account_account_user_permissions" ("account_id", "permission_id");
CREATE INDEX "Account_account_user_permissions_8a089c2a" ON "Account_account_user_permissions" ("account_id");
CREATE INDEX "Account_account_user_permissions_8373b171" ON "Account_account_user_permissions" ("permission_id");
CREATE INDEX "Account_seller_8a089c2a" ON "Account_seller" ("account_id");
COMMIT;


BEGIN;
--
-- Create model Address
--
CREATE TABLE "Info_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address1" varchar(200) NOT NULL, "address2" varchar(200) NOT NULL, "city" varchar(200) NOT NULL, "zip_code" integer NOT NULL, "state" varchar(200) NOT NULL);
--
-- Create model CreditCard
--
CREATE TABLE "Info_creditcard" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "number" integer NOT NULL, "expire_date" date NOT NULL, "cvv" integer NOT NULL, "address_id" integer NOT NULL REFERENCES "Info_address" ("id"));
CREATE INDEX "Info_creditcard_ea8e5d12" ON "Info_creditcard" ("address_id");
COMMIT;

BEGIN;
--
-- Create model BidItem
--
CREATE TABLE "Item_biditem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "start_time" datetime NOT NULL, "end_time" datetime NOT NULL, "reserved_price" integer NOT NULL, "action_price" integer NOT NULL);
--
-- Create model Category
--
CREATE TABLE "Item_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "level" integer NOT NULL, "name" varchar(200) NOT NULL, "childID_id" integer NOT NULL REFERENCES "Item_category" ("id"));
--
-- Create model Item
--
CREATE TABLE "Item_item" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "keywords" varchar(200) NOT NULL, "listed_price" integer NOT NULL, "bid_id" integer NULL UNIQUE REFERENCES "Item_biditem" ("id"));
--
-- Create model Order
--
CREATE TABLE "Item_order" ("created" datetime NOT NULL, "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "amount" integer NOT NULL, "buyer_id" integer NOT NULL REFERENCES "Account_account" ("id"), "item_id" integer NOT NULL REFERENCES "Item_item" ("id"));
--
-- Create model Rate
--
CREATE TABLE "Item_rate" ("created" datetime NOT NULL, "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "num" integer NOT NULL, "item_id" integer NOT NULL REFERENCES "Item_item" ("id"), "rater_id" integer NOT NULL REFERENCES "Account_account" ("id"));
CREATE INDEX "Item_category_d06f4efc" ON "Item_category" ("childID_id");
CREATE INDEX "Item_order_2c724d65" ON "Item_order" ("buyer_id");
CREATE INDEX "Item_order_82bfda79" ON "Item_order" ("item_id");
CREATE INDEX "Item_rate_82bfda79" ON "Item_rate" ("item_id");
CREATE INDEX "Item_rate_9e4fc8b5" ON "Item_rate" ("rater_id");
COMMIT;
