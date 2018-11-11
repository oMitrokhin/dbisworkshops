insert into "User" (user_email, user_password, user_information)
    values ('user@email.com', 'Qwerty123', 'test account');
    
insert into "User" (user_email, user_password, user_information)
    values ('userok@email.com', 'Pass55', '');
    
insert into "User" (user_email, user_password, user_information)
    values ('mail_51@email.com', 'Qwerty_ytrewq', 'Account for check holiday costs');

insert into Available_product (product_name, product_average_price)
    values ('Gibson Medium Guitar Pick', '0.45');
    
insert into Available_product (product_name, product_average_price)
    values ('Dunlop Tortex 0.73mm Guitar Pick', '0.69');
    
insert into Available_product (product_name, product_average_price)
    values ('Fender Classic Shell Medium Guitar Pick', '0.5');
   
insert into User_product (product_id, user_email, product_name, purchase_date, user_product_price, product_count, product_priority)
    values ('1', 'user@email.com', 'Dunlop Tortex 0.73mm Guitar Pick', to_date('2018-11-10', 'YYYY-MM-DD'), '0.71', '3', 'Medium');
    
insert into User_product (product_id, user_email, product_name, purchase_date, user_product_price, product_count, product_priority)
    values ('2', 'mail_51@email.com', 'Dunlop Tortex 0.73mm Guitar Pick', to_date('2018-11-03', 'YYYY-MM-DD'), '0.65', '20', 'High');
    
insert into User_product (product_id, user_email, product_name, purchase_date, user_product_price, product_count, product_priority)
    values ('3', 'mail_51@email.com', 'Fender Classic Shell Medium Guitar Pick', to_date('2018-11-11', 'YYYY-MM-DD'), '0.57', '2', 'Medium');

    