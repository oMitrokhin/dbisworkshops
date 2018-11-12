alter table User_product
   drop constraint FK_PRODUCT_SOLD;

alter table User_product
   drop constraint FK_USER_HAS_PRODUCT;

drop index "Products sold_FK";

drop index "User has products_FK";

drop table User_product cascade constraints;

drop table Available_product cascade constraints;

drop table "User" cascade constraints;

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User"
(
   user_email           VARCHAR2(30)         not null,
   user_password        VARCHAR2(20)         not null,
   user_information     CLOB,
   constraint PK_USER primary key (user_email)
);
/*==============================================================*/
/* Table: Available_product                                     */
/*==============================================================*/
create table Available_product 
(
   product_name         VARCHAR2(50)         not null,
   product_average_price FLOAT(10)            not null,
   constraint PK_AVAILABLE_PRODUCT primary key (product_name)
);

/*==============================================================*/
/* Table: User_product                                          */
/*==============================================================*/
create table User_product 
(
   product_id           INTEGER              not null,
   user_email           VARCHAR2(30)         not null,
   product_name         VARCHAR2(50)         not null,
   purchase_date        DATE                 not null,
   user_product_price   FLOAT(10)            not null,
   product_count        INTEGER              not null,
   product_priority     VARCHAR2(20)         not null,
   constraint PK_USER_PRODUCT primary key (product_id)
);

/*==============================================================*/
/* Index: "User has products_FK"                                */
/*==============================================================*/
create index "User has products_FK" on User_product (
   user_email ASC
);

/*==============================================================*/
/* Index: "Products sold_FK"                                    */
/*==============================================================*/
create index "Products sold_FK" on User_product (
   product_name ASC
);


alter table User_product
   add constraint FK_PRODUCT_SOLD foreign key (product_name)
      references Available_product (product_name);

alter table User_product
   add constraint FK_USER_HAS_PRODUCT foreign key (user_email)
      references "User" (user_email);
      
alter table "User"
    add constraint check_email 
    check (regexp_like (user_email, '\w{3,19}+@\w{1,7}+\.[a-z]{2,3}'));

alter table "User"
    add constraint check_user_password
    check (regexp_like (user_password, '[A-Z]+\w{1,18}+[A-Za-z0-9)]'));
    
alter table Available_product
    add constraint check_product_name
    check (regexp_like (product_name, '\w{1,50}'));
/*  
alter table Available_product
    add constraint check_product_average_price
    check (regexp_like (product_average_price, '\d{1,8}+\.+\d{1,2}'));
*/
alter table User_product
    add constraint check_purchase_date
    check (purchase_date > date '2000-01-01');
/*
alter table User_product
    add constraint check_user_product_price
    check (regexp_like (user_product_price, '\d{1,8}+\,+\d{1,2}'));
*/
alter table User_product
    add constraint check_product_priority
    check (regexp_like (product_priority, '\w{1,20}|\w{1,10}\b\w{1,9}'));
