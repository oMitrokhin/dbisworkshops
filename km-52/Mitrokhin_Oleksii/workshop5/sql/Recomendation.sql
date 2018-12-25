create or replace package P_Recomendation is
type r_recomendation is record(
    product_name Available_product.product_name%type,
    product_total_price FLOAT(15),
    product_count INTEGER,
    product_priority User_product.product_priority%type
);
type tb_recommendation is table of r_recomendation;

function get_recomendation(chek_email in User_product.user_email%type, start_date User_product.purchase_date%type, end_date User_product.purchase_date%type, total_count integer)
return tb_recomendation
pipelined;

end P_Recomendation;

create or replace package body P_Recomendation is

function get_recomendation(check_email in User_product.user_email%type, start_date in User_product.purchase_date%type, end_date in User_product.purchase_date%type, total_count in integer)
return tb_recomendation
pipelined is
cursor recomendation_curr is
select
product_name,
product_priority,
sum(user_product_price*product_count) as total_price,
sum(product_count) as product_total_count
from User_product
where user_email = check_email and purchase_date between start_date and end_date
group by product_priority, product_name
order by field(product_priority, 'Low','Medium','High'), total_price desc;
begin
for curr in recomendation_curr
loop
pipe row(curr);
total_count := total_count-1;
exit when(total_count<=0);
end loop;
end get_recomendation;
end;

