create or replace package P_User is
type row_user is record(
user_email "User".user_email%type,
user_password "User".user_password%type,
user_information "User".user_information%type,
user_role "User".Role%type
);

Type tb_row_user is table of row_user;

function get_user(email in "User".user_email%type)
return row_user;

--procedure block_un_user (email in User_product.user_email%type);
procedure edit_user (email in "User".user_email%type, user_pass in "User".user_password%type, information in "User".user_information%type);
end P_User;
/
create or replace package body P_User is

function get_user(email in "User".user_email%type)
return row_user
is
search_user row_user;
begin
    select * into search_user
    from "User"
    where user_email = email;
    
    if email!=search_user.user_email then
        return NULL;
    end if;
    return  search_user;
end get_user;
/*
procedure block_un_user (email in User_product.user_email%type)
is
begin
if 'User' in (select role from "User" where user_email = email) then
    update "User"
        set role='Banned'
    where user_email = email;
else if 'Banned' in (select role from "User" where user_email = email) then
    update "User"
    set role='User'
    where user_email = email;
end if;
end;
*/
procedure edit_user (email in "User".user_email%type, user_pass in "User".user_password%type, information in "User".user_information%type)
is
begin
update "User"
    set user_password=user_pass, user_information=information
where user_email = email;
end;

end P_User;