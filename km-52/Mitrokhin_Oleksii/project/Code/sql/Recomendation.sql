create or replace package P_Recomendation is
type r_recomendation is record(
    product_name Available_product.product_name%type,
    product_total_price FLOAT(15),
    product_count INTEGER,
    product_priority User_product.product_priority%type
);
type tb_recomendation is table of r_recomendation;

function get_recomendation(check_email in User_product.user_email%type, start_date in User_product.purchase_date%type, end_date in User_product.purchase_date%type, total_count in integer)
return tb_recomendation
pipelined;

end P_Recomendation;
/
create or replace package body P_Recomendation is

function get_recomendation(check_email in User_product.user_email%type, start_date in User_product.purchase_date%type, end_date in User_product.purchase_date%type, total_count in integer)
return tb_recomendation
pipelined is
cursor recomendation_curr is
select
product_name,
sum(user_product_price*product_count) as total_price,   
sum(product_count) as product_total_count,
product_priority
from User_product
where user_email = check_email and purchase_date between start_date and end_date
group by product_priority, product_name
order by case product_priority
when 'Low' then 1 when 'Medium' then 2 when 'High' then 3 end,
total_price desc;
curr r_recomendation;
counter int;
begin
counter :=total_count;
open recomendation_curr;
while counter>0
--for curr in recomendation_curr
loop
fetch recomendation_curr into curr;
exit when recomendation_curr%NOTFOUND;
pipe row(curr);
counter := counter-1;
--exit when(total_count<=0);
end loop;
close recomendation_curr;
end get_recomendation;
end;

