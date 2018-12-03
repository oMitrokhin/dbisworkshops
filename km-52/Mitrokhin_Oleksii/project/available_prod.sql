create or replace package P_Av_PR is
type r_available_product is record(
    product_name Available_product.product_name%type,
    product_average_price Available_product.product_average_price%type
);

type tb_available_product is table of r_available_product;

function get_available_product
return tb_available_product
pipelined;
procedure add_product_to_base (product_name in Available_product.product_name%type, product_price in Available_product.product_average_price%type);
procedure delete_product_from_base (d_product_name in User_product.product_name%type);

end P_Av_PR;