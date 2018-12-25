insert into Role (role)
    values('Banned');
insert into Role (role)
    values('Admin');
insert into Role (role)
    Values('User');

insert into "User" (user_email, role, user_password, user_information)
    values ('user@email.com','User', 'Qwerty123', 'test account');
    
insert into "User" (user_email, role, user_password, user_information)
    values ('userok@email.com','Admin', 'Pass55', 'Admin');
    
insert into "User" (user_email, role, user_password, user_information)
    values ('mail_51@email.com','User', 'Qwerty_ytrewq', 'Account for check holiday costs');

insert into Available_product (product_name, product_average_price)
    values ('Gibson Medium Guitar Pick', '0.45');
    
insert into Available_product (product_name, product_average_price)
    values ('Dunlop Tortex 0.73mm Guitar Pick', '0.69');
    
insert into Available_product (product_name, product_average_price)
    values ('Fender Classic Shell Medium Guitar Pick', '0.5');
   
insert into User_product (user_email, product_name, purchase_date, user_product_price, product_count, product_priority)
    values ('user@email.com', 'Dunlop Tortex 0.73mm Guitar Pick', to_date('2018-11-10', 'YYYY-MM-DD'), '0.71', '3', 'Medium');
    
insert into User_product (user_email, product_name, purchase_date, user_product_price, product_count, product_priority)
    values ('mail_51@email.com', 'Dunlop Tortex 0.73mm Guitar Pick', to_date('2018-11-03', 'YYYY-MM-DD'), '0.65', '20', 'High');
    
insert into User_product (user_email, product_name, purchase_date, user_product_price, product_count, product_priority)
    values ('mail_51@email.com', 'Fender Classic Shell Medium Guitar Pick', to_date('2018-11-11', 'YYYY-MM-DD'), '0.57', '2', 'Medium');
   