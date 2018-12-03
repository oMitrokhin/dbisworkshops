create or replace package P_user_product is
type user_product_list is record(
    product_name Available_product.product_name%type,
    user_product_price float(10),
    purchase_date date,
    product_priority User_product.product_priority%type,
    product_count integer
);

type tb_user_product is table of user_product_list;

function get_user_product(email in User_product.user_email%type)
return tb_user_product
pipelined;
procedure add_product_to_userbase (user_email in User_product.user_email%type, product_name in User_product.product_name%type, purchase_date in User_product.purchase_date%type, user_product_price in User_product.user_product_price%type, product_count in User_product.product_count%type, product_priority in User_product.product_priority%type);
procedure delete_user_product (email in User_product.user_email%type, d_product_name in User_product.product_name%type, d_purchase_date in User_product.purchase_date%type);
procedure edit_product_in_userbase (email in User_product.user_email%type, product_name in User_product.product_name%type, purchase_date in User_product.purchase_date%type, user_product_price in User_product.user_product_price%type, product_count in User_product.product_count%type, product_priority in User_product.product_priority%type);
end P_user_product;