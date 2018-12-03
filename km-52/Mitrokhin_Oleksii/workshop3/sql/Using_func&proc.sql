SET SERVEROUTPUT ON
begin
P_user_product.add_product_to_userbase('user@email.com','Fender Classic Shell Medium Guitar Pick', to_date('2018-12-3', 'YYYY-MM-DD'), '0.57', '2', 'Medium'); 
P_user_product.delete_user_product('user@email.com','Fender Classic Shell Medium Guitar Pick', '03-DEC-18'); 
P_user_product.edit_product_in_userbase('mail_51@email.com', 'Dunlop Tortex 0.73mm Guitar Pick', to_date('2018-12-3', 'YYYY-MM-DD'), '1', '15', 'High'); 
dbms_output.put_line(P_user_product.get_user_product('mail_51@email.com')); 

end;