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

create or replace package body P_user_product is

function get_user_product(email in User_product.user_email%type)
return tb_user_product
        pipelined is
            cursor user_product_cur is
            select 
            product_name, user_product_price, purchase_date, product_priority,  product_count
            from User_product
            where User_product.user_email = email;
            begin
            for curr in user_product_cur
            loop
                pipe row(curr);
            end loop;    
            end get_user_product;
    
procedure add_product_to_userbase (user_email in User_product.user_email%type, product_name in User_product.product_name%type, purchase_date in User_product.purchase_date%type, user_product_price in User_product.user_product_price%type, product_count in User_product.product_count%type, product_priority in User_product.product_priority%type)
is
begin
insert into User_product(user_email, product_name, purchase_date, user_product_price, product_count, product_priority)
values(user_email, product_name, purchase_date, user_product_price, product_count, product_priority);
end;
procedure delete_user_product (email in User_product.user_email%type, d_product_name in User_product.product_name%type, d_purchase_date in User_product.purchase_date%type)
is
begin
delete from User_product
where user_email=email and product_name=d_product_name and purchase_date=d_purchase_date;
end;
procedure edit_product_in_userbase (email in User_product.user_email%type, product_name in User_product.product_name%type, purchase_date in User_product.purchase_date%type, user_product_price in User_product.user_product_price%type, product_count in User_product.product_count%type, product_priority in User_product.product_priority%type)
is
begin
update User_product
set user_product_price=user_product_price, product_count=product_count, product_priority=product_priority
where user_email = email and product_name=product_name and purchase_date=purchase_date;
end;

end;